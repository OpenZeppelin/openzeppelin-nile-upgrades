import click

from nile.core.account import Account
from nile.nre import NileRuntimeEnvironment
from nile import deployments

from nile_upgrades import declare_impl

@click.command()
@click.argument("signer", type=str)
@click.argument("proxy_identifier", type=str)
@click.argument("contract_name", type=str)
@click.option("--max_fee", nargs=1)
def upgrade_proxy(proxy_identifier, contract_name, signer, max_fee=None):
    """
    Upgrade a proxy to a different implementation contract.
    """

    nre = NileRuntimeEnvironment()

    ids = deployments.load(proxy_identifier, nre.network)
    id = next(ids, None)
    if id is None:
        raise Exception(f"Deployment with address or alias {proxy_identifier} not found")
    if next(ids, None) is not None:
        raise Exception(f"Multiple deployments found with address or alias {proxy_identifier}")

    proxy_address = id[0]

    hash = declare_impl.declare_impl(nre, contract_name, signer, max_fee)

    click.echo(f"Upgrading proxy {proxy_address}...")
    account = Account(signer, nre.network)
    account.send(proxy_address, "upgrade", calldata=[int(hash, 16)], max_fee=max_fee)
    click.echo(f"Proxy upgraded to implementation with hash {hash}")

    deployments.update(proxy_address, f"artifacts/abis/{contract_name}.json", nre.network)
