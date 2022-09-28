from email.policy import default
import click
import os

from nile.nre import NileRuntimeEnvironment
from starkware.starknet.compiler.compile import get_selector_from_name

from nile_upgrades import declare_impl

@click.command()
@click.argument("signer", type=str)
@click.argument("contract_name", type=str)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--initializer", nargs=1, default="initializer")
@click.option("--max_fee", nargs=1)
def deploy_proxy(contract_name, signer, initializer, args, max_fee=None):
    """
    Deploy an upgradeable proxy for an implementation contract.
    """

    nre = NileRuntimeEnvironment()

    hash = declare_impl.declare_impl(nre, contract_name, signer, max_fee)

    click.echo(f"Deploying upgradeable proxy...")
    selector = get_selector_from_name(initializer)
    addr, abi = nre.deploy("Proxy", arguments=[hash, selector, len(args), *args], overriding_path=get_proxy_artifact_path(), abi=f"artifacts/abis/{contract_name}.json")
    click.echo(f"Proxy deployed to address {addr}, abi {abi}")

    return addr

def get_proxy_artifact_path():
    pt = os.path.dirname(os.path.realpath(__file__)).replace("/nile_upgrades", "")
    return (f"{pt}/artifacts", f"{pt}/artifacts/abis")
