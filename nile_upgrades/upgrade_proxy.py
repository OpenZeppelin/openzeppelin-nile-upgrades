import click

from nile.nre import NileRuntimeEnvironment
from nile import deployments
from nile.deployments import HashExistsException


@click.command()
@click.argument("proxy_address", type=str)
@click.argument("contract_name", type=str)
def upgrade_proxy(proxy_address, contract_name):
    """
    Upgrade a proxy to a different implementation contract.
    """

    nre = NileRuntimeEnvironment()

    click.echo(f"Declaring implementation {contract_name}...")
    hash = None
    try:
        hash = nre.declare(contract_name)
        click.echo(f"Implementation declared with hash {hash}")
    except HashExistsException as e:
        hash = e.hash
        click.echo(f"Implementation with hash {hash} already exists")

    click.echo(f"Upgrading proxy...")
    nre.invoke(proxy_address, "upgrade", params=[hash])
    click.echo(f"Proxy upgraded to implementation with hash {hash}")

    deployments.update(proxy_address, f"artifacts/abis/{contract_name}.json", nre.network, alias=None)
