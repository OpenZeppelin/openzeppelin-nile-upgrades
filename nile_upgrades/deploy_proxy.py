import click
import os

from nile.nre import NileRuntimeEnvironment

from nile_upgrades import declare_impl

@click.command()
@click.argument("contract_name", type=str)
def deploy_proxy(contract_name):
    """
    Deploy an upgradeable proxy for an implementation contract.
    """

    nre = NileRuntimeEnvironment()

    hash = declare_impl.declare_impl(nre, contract_name)

    click.echo(f"Deploying upgradeable proxy...")
    addr, abi = nre.deploy("Proxy", arguments=[hash], overriding_path=get_proxy_artifact_path(), abi=f"artifacts/abis/{contract_name}.json")
    click.echo(f"Proxy deployed to address {addr}, abi {abi}")

    return addr

def get_proxy_artifact_path():
    pt = os.path.dirname(os.path.realpath(__file__)).replace("/nile_upgrades", "")
    return (f"{pt}/artifacts", f"{pt}/artifacts/abis")
