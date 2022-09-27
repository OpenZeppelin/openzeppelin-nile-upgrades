import click

from nile.deployments import class_hash_exists

from nile.common import ABIS_DIRECTORY, BUILD_DIRECTORY
from nile.core.account import Account
from nile.utils import get_hash

def declare_impl(nre, contract_name, signer):
    """
    Declare an implementation contract.
    """
    click.echo(f"Declaring implementation {contract_name}...")
    hash = get_hash(contract_name=contract_name, )
    if class_hash_exists(hash, nre.network):
        click.echo(f"Implementation with hash {hash} already exists")
    else:
        account = Account(signer, nre.network)
        declared_hash = account.declare(contract_name, max_fee=0) # TODO
        if hash != declared_hash:
            raise Exception(f"Declared hash {declared_hash} does not match expected hash {hash}")
        click.echo(f"Implementation declared with hash {declared_hash}")

    return hash
