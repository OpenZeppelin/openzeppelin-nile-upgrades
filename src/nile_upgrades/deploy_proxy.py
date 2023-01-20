import logging
import os

from starkware.starknet.compiler.compile import get_selector_from_name

from nile_upgrades.common import declare_class, get_contract_abi


async def deploy_proxy(
    nre,
    account,
    contract_name,
    salt,
    unique,
    initializer_args,
    initializer='initializer',
    alias=None,
    max_fee_declare_impl=None,
    max_fee_declare_proxy=None,
    max_fee_deploy_proxy=None,
    standalone_mode=None
):
    """
    Deploy an upgradeable proxy for an implementation contract.

    Returns a Nile Transaction instance representing the proxy deployment.

    `nre` - the `NileRuntimeEnvironment` object.

    `account` - the Account to use.

    `contract_name` - the name of the implementation contract.

    `salt` and `unique` - UDC specific arguments for proxy address generation.

    `initializer_args` - array of arguments for the initializer function.

    `initializer` - initializer function name. Defaults to `'initializer'`.

    `alias` - Unique identifier for your proxy. Defaults to `None`.

    `max_fee_declare_impl` - Maximum fee for declaring the implementation contract. Defaults to `None`.

    `max_fee_declare_proxy` - Maximum fee for declaring the proxy contract. Defaults to `None`.

    `max_fee_deploy_proxy` - Maximum fee for deploying the proxy contract. Defaults to `None`.
    """

    # Declare implementation
    impl_class_hash = await declare_class(nre.network, contract_name, account, max_fee_declare_impl)

    # Declare proxy
    await declare_class(nre.network, "Proxy", account, max_fee_declare_proxy, overriding_path=_get_proxy_artifact_path())

    # Deploy proxy
    logging.debug(f"Deploying proxy...")
    selector = get_selector_from_name(initializer)
    deploy_tx = await account.deploy_contract(
        "Proxy",
        salt=salt,
        unique=unique,
        calldata=[impl_class_hash, selector, len(initializer_args), *initializer_args],
        max_fee=max_fee_deploy_proxy,
        alias=alias,
        overriding_path=_get_proxy_artifact_path(),
        abi=get_contract_abi(contract_name),
    )

    return deploy_tx


def _get_proxy_artifact_path():
    package = os.path.dirname(os.path.realpath(__file__))
    return (f"{package}/artifacts", f"{package}/artifacts/abis")
