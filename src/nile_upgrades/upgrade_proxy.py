import logging

from nile import deployments
from nile.common import is_alias
from nile.core.account import Account
from nile.nre import NileRuntimeEnvironment
from nile.utils import normalize_number, hex_class_hash, hex_address

from nile_upgrades import common


def upgrade_proxy(signer, proxy_address_or_alias, contract_name, max_fee=None, standalone_mode=None):
    """
    Upgrade a proxy to a different implementation contract.

    `signer` - private key alias for the Account to use.

    `proxy_address_or_alias` - the proxy address or alias.

    `contract_name` - the name of the implementation contract to upgrade to.

    `max_fee` - Maximum fee for the transaction. Defaults to `None`.
    """

    nre = NileRuntimeEnvironment()

    proxy_address = _load_deployment(proxy_address_or_alias, nre.network)

    impl_class_hash = common.declare_impl(nre, contract_name, signer, max_fee)

    logging.info(f"⏭️  Upgrading proxy {hex_address(proxy_address)} to class hash {hex_class_hash(impl_class_hash)}")
    account = Account(signer, nre.network)
    upgrade_result = account.send(
        proxy_address, "upgrade", calldata=[impl_class_hash], max_fee=max_fee
    )

    tx_hash = _get_tx_hash(upgrade_result)
    logging.info(f"🧾 Upgrade transaction hash: {tx_hash}")

    deployments.update_abi(
        proxy_address, common.get_contract_abi(contract_name), nre.network
    )

    return tx_hash


def _load_deployment(proxy_address_or_alias, network):
    ids = None
    if not is_alias(proxy_address_or_alias):
        ids = deployments.load(normalize_number(proxy_address_or_alias), network)
    else:
        ids = deployments.load(proxy_address_or_alias, network)

    id = next(ids, None)
    if id is None:
        raise Exception(
            f"Deployment with address or alias {proxy_address_or_alias} not found"
        )
    if next(ids, None) is not None:
        raise Exception(
            f"Multiple deployments found with address or alias {proxy_address_or_alias}"
        )

    return id[0]


def _get_tx_hash(output):
    lines = output.splitlines()
    for line in lines:
        if "Transaction hash" in line:
            return line.split(":")[1].strip()
