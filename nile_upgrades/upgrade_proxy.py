import click
import logging

from nile.core.account import Account
from nile.nre import NileRuntimeEnvironment
from nile import deployments

from nile_upgrades import declare_impl

@click.command()
@click.argument("signer", type=str)
@click.argument("proxy_address_or_alias", type=str)
@click.argument("contract_name", type=str)
@click.option("--max_fee", nargs=1, help="Maximum fee for the transaction. Defaults to 0.")
def upgrade_proxy(proxy_address_or_alias, contract_name, signer, max_fee=None):
    """
    Upgrade a proxy to a different implementation contract.

    SIGNER - private key alias for the Account to use.

    PROXY_ADDRESS_OR_ALIAS - the proxy address or alias.

    CONTRACT_NAME - the name of the implementation contract to upgrade to.
    """

    nre = NileRuntimeEnvironment()

    ids = deployments.load(proxy_address_or_alias, nre.network)
    id = next(ids, None)
    if id is None:
        raise Exception(f"Deployment with address or alias {proxy_address_or_alias} not found")
    if next(ids, None) is not None:
        raise Exception(f"Multiple deployments found with address or alias {proxy_address_or_alias}")

    proxy_address = id[0]

    hash = declare_impl.declare_impl(nre, contract_name, signer, max_fee)

    logging.info(f"⏭️  Upgrading proxy {proxy_address} to class hash {hash}")
    account = Account(signer, nre.network)
    upgrade_result = account.send(proxy_address, "upgrade", calldata=[int(hash, 16)], max_fee=max_fee)

    txhash = get_tx_hash(upgrade_result)
    logging.info(f"🧾 Upgrade transaction hash: {txhash}")

    deployments.update(proxy_address, f"artifacts/abis/{contract_name}.json", nre.network)

    return txhash


def get_tx_hash(output):
    lines = output.splitlines()
    for line in lines:
        if "Transaction hash" in line:
            return line.split(":")[1].strip()