import logging
import os

from starkware.starknet.compiler.compile import get_selector_from_name

from nile.utils import hex_address

from nile_upgrades.common import declare_impl, get_contract_abi


async def deploy_proxy(
    nre, signer, contract_name, initializer_args, initializer='initializer', alias=None, max_fee=None, standalone_mode=None
):
    """
    Deploy an upgradeable proxy for an implementation contract.

    `nre` - the `NileRuntimeEnvironment` object.

    `signer` - private key alias for the Account to use.

    `contract_name` - the name of the implementation contract.

    `initializer_args` - array of arguments for the initializer function.

    `initializer` - initializer function name. Defaults to `'initializer'`.

    `alias` - Unique identifier for your proxy. Defaults to `None`.

    `max_fee` - Maximum fee for the transaction. Defaults to `None`.
    """

    impl_class_hash = await declare_impl(nre.network, contract_name, signer, max_fee)

    logging.debug(f"Deploying upgradeable proxy...")
    selector = get_selector_from_name(initializer)
    addr, abi = await nre.deploy(
        "Proxy",
        arguments=[impl_class_hash, selector, len(initializer_args), *initializer_args],
        alias=alias,
        overriding_path=_get_proxy_artifact_path(),
        abi=get_contract_abi(contract_name),
    )
    logging.debug(f"Proxy deployed to address {hex_address(addr)} using ABI {abi}")

    return addr


def _get_proxy_artifact_path():
    package = os.path.dirname(os.path.realpath(__file__))
    return (f"{package}/artifacts", f"{package}/artifacts/abis")
