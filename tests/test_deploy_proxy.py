"""Tests for deploy proxy."""
import os
import pytest
from unittest.mock import patch

from nile.nre import NileRuntimeEnvironment
from nile.utils.status import TransactionStatus, TxStatus

from nile_upgrades.common import get_contract_abi
from nile_upgrades.deploy_proxy import deploy_proxy

from mocks.mock_account import MockAccount


NETWORK = "localhost"
CONTRACT = "contract"
SIGNER = "PKEY1"

SELECTOR = 1
CLASS_HASH = 16
PROXY_CLASS_HASH = 17
ARGS = ["abc", 123]
PROXY_ADDR = "0x000000000000000000000000000000000000000000000000000000000000000f"
PROXY_ADDR_INT = 15
PROXY_ARTIFACT_PATH = ("upgrades/artifacts", "upgrades/artifacts/abis")
IMPL_ABI = get_contract_abi(CONTRACT)

SALT_DEFAULT = 0
UNIQUE_DEFAULT = False

SALT = 10
UNIQUE = True

CUSTOM_INIT = "my_init_func"
ALIAS = "my_alias"
MAX_FEE_DECLARE_IMPL = 100
MAX_FEE_DECLARE_PROXY = 200
MAX_FEE_DEPLOY_PROXY = 300

KEY = "TEST_KEY"
PRIVATE_KEY = "1234"
MOCK_TX_HASH = 1
TX_STATUS = TransactionStatus(MOCK_TX_HASH, TxStatus.ACCEPTED_ON_L2, None)


@pytest.mark.asyncio
@patch("nile_upgrades.deploy_proxy.declare_class")
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
@patch("nile.core.types.account.Account.deploy_contract")
async def test_deploy_proxy(
    mock_deploy, mock_get_proxy_artifact_path, mock_get_selector, mock_declare_class
):
    mock_declare_class.side_effect = [CLASS_HASH, PROXY_CLASS_HASH]

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await deploy_proxy(NileRuntimeEnvironment(), account, CONTRACT, ARGS)

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_class, account, "initializer", PROXY_ARTIFACT_PATH, SALT_DEFAULT, UNIQUE_DEFAULT, None, None, None, None)


@pytest.mark.asyncio
@patch("nile_upgrades.deploy_proxy.declare_class")
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
@patch("nile.core.types.account.Account.deploy_contract")
async def test_deploy_proxy_all_opts(
    mock_deploy, mock_get_proxy_artifact_path, mock_get_selector, mock_declare_class
):
    mock_declare_class.side_effect = [CLASS_HASH, PROXY_CLASS_HASH]

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await deploy_proxy(NileRuntimeEnvironment(), account, CONTRACT, ARGS, CUSTOM_INIT, SALT, UNIQUE, ALIAS, MAX_FEE_DECLARE_IMPL, MAX_FEE_DECLARE_PROXY, MAX_FEE_DEPLOY_PROXY)

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_class, account, CUSTOM_INIT, PROXY_ARTIFACT_PATH, SALT, UNIQUE, ALIAS, MAX_FEE_DECLARE_IMPL, MAX_FEE_DECLARE_PROXY, MAX_FEE_DEPLOY_PROXY)


def _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_class, account, initializer, overriding_path, salt, unique, alias, max_fee_declare_impl, max_fee_declare_proxy, max_fee_deploy_proxy):
    mock_declare_class.assert_any_call(NETWORK, CONTRACT, account, max_fee_declare_impl)
    mock_declare_class.assert_any_call(NETWORK, "Proxy", account, max_fee_declare_proxy, overriding_path=overriding_path)

    mock_get_selector.assert_called_once_with(initializer)

    mock_deploy.assert_called_once_with(
        "Proxy",
        salt=salt,
        unique=unique,
        calldata=[CLASS_HASH, SELECTOR, len(ARGS), *ARGS],
        max_fee=max_fee_deploy_proxy,
        alias=alias,
        overriding_path=PROXY_ARTIFACT_PATH,
        abi=IMPL_ABI,
    )
