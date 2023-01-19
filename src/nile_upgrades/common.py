import logging

from nile.common import get_class_hash, ABIS_DIRECTORY
from nile.deployments import class_hash_exists
from nile.utils import hex_class_hash


async def declare_class(network, contract_name, account, max_fee, overriding_path=None):
    """
    Declare a contract class and waits until the transaction completes.

    Returns the declared class hash in decimal format.
    """
    logging.debug(f"Declaring contract class {contract_name}...")
    class_hash = get_class_hash(contract_name=contract_name, overriding_path=overriding_path)
    padded_hash = hex_class_hash(class_hash)
    if class_hash_exists(class_hash, network):
        logging.debug(f"Contract class with hash {padded_hash} already exists")
    else:
        tx = await account.declare(contract_name, max_fee=max_fee, overriding_path=overriding_path)
        tx_status, declared_hash = await tx.execute(watch_mode="track")

        if tx_status.status.is_rejected:
            raise Exception(f"Could not declare contract class. Transaction rejected.", tx_status.error_message)

        if padded_hash != declared_hash:
            raise Exception(
                f"Declared hash {declared_hash} does not match expected hash {padded_hash}"
            )

        logging.debug(f"Contract class declared with hash {padded_hash}")

    return class_hash


def get_contract_abi(contract_name):
    return f"{ABIS_DIRECTORY}/{contract_name}.json"
