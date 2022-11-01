import logging

from nile.common import get_hash
from nile.core.account import Account
from nile.deployments import class_hash_exists


def declare_impl(nre, contract_name, signer, max_fee):
    """
    Declare an implementation contract.
    """
    logging.debug(f"Declaring implementation {contract_name}...")
    hash = get_hash(contract_name=contract_name)
    if class_hash_exists(hash, nre.network):
        logging.debug(f"Implementation with hash {hash} already exists")
    else:
        account = Account(signer, nre.network)
        declared_hash = account.declare(contract_name, max_fee=max_fee)
        if hash != declared_hash:
            raise Exception(
                f"Declared hash {declared_hash} does not match expected hash {hash}"
            )
        logging.debug(f"Implementation declared with hash {declared_hash}")

    return hash
