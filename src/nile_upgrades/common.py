import logging

from nile.common import get_hash, ABIS_DIRECTORY
from nile.core.account import Account
from nile.deployments import class_hash_exists, normalize_number


def declare_impl(nre, contract_name, signer, max_fee):
    """
    Declare an implementation contract.
    """
    logging.debug(f"Declaring implementation {contract_name}...")
    padded_hash = get_hash(contract_name=contract_name)
    class_hash = normalize_number(padded_hash)
    if class_hash_exists(class_hash, nre.network):
        logging.debug(f"Implementation with hash {padded_hash} already exists")
    else:
        account = Account(signer, nre.network)
        declared_hash = account.declare(contract_name, max_fee=max_fee)
        if padded_hash != declared_hash:
            raise Exception(
                f"Declared hash {declared_hash} does not match expected hash {padded_hash}"
            )
        logging.debug(f"Implementation declared with hash {padded_hash}")

    return class_hash


def get_contract_abi(contract_name):
    return f"{ABIS_DIRECTORY}/{contract_name}.json"