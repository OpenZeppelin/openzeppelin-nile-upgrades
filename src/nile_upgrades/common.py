import logging

from nile.common import get_class_hash, ABIS_DIRECTORY
from nile.core.account import Account
from nile.deployments import class_hash_exists
from nile.utils import hex_class_hash


async def declare_impl(network, contract_name, signer, max_fee):
    """
    Declare an implementation contract.
    """
    logging.debug(f"Declaring implementation {contract_name}...")
    class_hash = get_class_hash(contract_name=contract_name)
    padded_hash = hex_class_hash(class_hash)
    if class_hash_exists(class_hash, network):
        logging.debug(f"Implementation with hash {padded_hash} already exists")
    else:
        account = await Account(signer, network)
        declared_hash = await account.declare(contract_name, max_fee=max_fee)
        if padded_hash != declared_hash:
            raise Exception(
                f"Declared hash {declared_hash} does not match expected hash {padded_hash}"
            )
        logging.debug(f"Implementation declared with hash {padded_hash}")

    return class_hash


def get_contract_abi(contract_name):
    return f"{ABIS_DIRECTORY}/{contract_name}.json"
