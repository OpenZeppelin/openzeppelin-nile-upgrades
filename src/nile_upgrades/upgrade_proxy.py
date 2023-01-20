import logging

from nile import deployments
from nile.common import is_alias
# from nile.core.account import Account
from nile.utils import normalize_number, hex_class_hash, hex_address

from nile_upgrades.common import declare_class, get_contract_abi


async def upgrade_proxy(
    nre,
    account,
    proxy_address_or_alias,
    contract_name,
    max_fee_declare_impl=None,
    max_fee_upgrade_proxy=None,
    standalone_mode=None
):
    """
    Upgrade a proxy to a different implementation contract.

    Returns a Nile Transaction instance representing the upgrade operation.

    `nre` - the `NileRuntimeEnvironment` object.

    `account` - the Account to use.

    `proxy_address_or_alias` - the proxy address or alias.

    `contract_name` - the name of the implementation contract to upgrade to.

    `max_fee_declare_impl` - Maximum fee for declaring the new implementation contract. Defaults to `None`.

    `max_fee_upgrade_proxy` - Maximum fee for upgrading the proxy to the new implementation. Defaults to `None`.
    """

    proxy_address = _load_deployment(proxy_address_or_alias, nre.network)

    # Declare new implementation
    impl_class_hash = await declare_class(nre.network, contract_name, account, max_fee_declare_impl)

    # Perform upgrade
    logging.info(f"⏭️  Upgrading proxy {hex_address(proxy_address)} to class hash {hex_class_hash(impl_class_hash)}")
    upgrade_tx = await account.send(
        proxy_address, "upgrade", calldata=[impl_class_hash], max_fee=max_fee_upgrade_proxy
    )

    # Update ABI in deployments file
    deployments.update_abi(
        proxy_address, get_contract_abi(contract_name), nre.network
    )

    return upgrade_tx


def _load_deployment(proxy_address_or_alias, network):
    ids = None
    if not is_alias(proxy_address_or_alias):
        ids = deployments.load(normalize_number(proxy_address_or_alias), network)
    else:
        ids = deployments.load(proxy_address_or_alias, network)

    id = next(ids, None)
    if id is None:
        raise Exception(
            f"Deployment with address or alias {_normalize_string(proxy_address_or_alias)} not found"
        )
    if next(ids, None) is not None:
        raise Exception(
            f"Multiple deployments found with address or alias {_normalize_string(proxy_address_or_alias)}"
        )

    return id[0]


def _normalize_string(proxy_address_or_alias):
    identifier = proxy_address_or_alias
    if type(identifier) is int:
        identifier = hex_address(identifier)
    return identifier
