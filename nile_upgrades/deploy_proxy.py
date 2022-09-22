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
    pt = os.path.dirname(os.path.realpath(__file__)).replace("/nile_upgrades", "")
    overriding_path = (f"{pt}/artifacts", f"{pt}/artifacts/abis")
    overriding_abi = f"artifacts/abis/{contract_name}.json";
    addr, abi = nre.deploy("Proxy", arguments=[hash], overriding_path=overriding_path, abi=overriding_abi)
    click.echo(f"Proxy deployed to address {addr}, abi {abi}")

    return addr
