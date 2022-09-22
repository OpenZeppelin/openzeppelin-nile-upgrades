import click

from starkware.crypto.signature.fast_pedersen_hash import pedersen_hash
from starkware.starknet.core.os.class_hash import compute_class_hash
from starkware.starknet.services.api.contract_class import ContractClass

from nile.nre import NileRuntimeEnvironment
from nile import deployments

from nile_upgrades import declare_impl

@click.command()
@click.argument("proxy_address", type=str)
@click.argument("contract_name", type=str)
def upgrade_proxy(proxy_address, contract_name):
    """
    Upgrade a proxy to a different implementation contract.
    """

    nre = NileRuntimeEnvironment()

    hash = declare_impl.declare_impl(nre, contract_name)

    click.echo(f"Upgrading proxy...")
    nre.invoke(proxy_address, "upgrade", params=[hash])
    click.echo(f"Proxy upgraded to implementation with hash {hash}")

    deployments.update(proxy_address, f"artifacts/abis/{contract_name}.json", nre.network, alias=None)
