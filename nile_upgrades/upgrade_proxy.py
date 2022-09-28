import click

from nile.core.account import Account
from nile.nre import NileRuntimeEnvironment
from nile import deployments

from nile_upgrades import declare_impl

@click.command()
@click.argument("signer", type=str)
@click.argument("proxy_address", type=str)
@click.argument("contract_name", type=str)
@click.option("--max_fee", nargs=1)
def upgrade_proxy(proxy_address, contract_name, signer, max_fee=None):
    """
    Upgrade a proxy to a different implementation contract.
    """

    nre = NileRuntimeEnvironment()

    hash = declare_impl.declare_impl(nre, contract_name, signer, max_fee)

    click.echo(f"Upgrading proxy...")
    account = Account(signer, nre.network)
    account.send(proxy_address, "upgrade", calldata=[int(hash, 16)], max_fee=max_fee)
    click.echo(f"Proxy upgraded to implementation with hash {hash}")

    deployments.update(proxy_address, f"artifacts/abis/{contract_name}.json", nre.network, alias=None)
