import click

from nile.deployments import class_hash_exists

from nile.common import ABIS_DIRECTORY, BUILD_DIRECTORY

from starkware.crypto.signature.fast_pedersen_hash import pedersen_hash
from starkware.starknet.core.os.class_hash import compute_class_hash
from starkware.starknet.services.api.contract_class import ContractClass

def declare_impl(nre, contract_name):
    """
    Declare an implementation contract.
    """
    click.echo(f"Declaring implementation {contract_name}...")
    hash = get_hash(contract_name=contract_name)
    if class_hash_exists(hash, nre.network):
        click.echo(f"Implementation with hash {hash} already exists")
    else:
        declared_hash = nre.declare(contract_name)
        if hash != declared_hash:
            raise Exception(f"Declared hash {declared_hash} does not match expected hash {hash}")
        click.echo(f"Implementation declared with hash {declared_hash}")

    return hash

def get_hash(contract_name, overriding_path=None):
    """Return the class hash (in hex) of a given contract class."""
    base_path = (
        overriding_path if overriding_path else (BUILD_DIRECTORY, ABIS_DIRECTORY)
    )
    with open(f"{base_path[0]}/{contract_name}.json", "r") as fp:
        contract_class = ContractClass.loads(fp.read())

    return hex(compute_class_hash(contract_class=contract_class, hash_func=pedersen_hash))
