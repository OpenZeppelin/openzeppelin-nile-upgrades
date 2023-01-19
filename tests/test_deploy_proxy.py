"""Tests for deploy proxy."""
import os
from unittest.mock import AsyncMock, call, patch

from nile.nre import NileRuntimeEnvironment
import pytest
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

CUSTOM_INIT = "my_init_func"
ALIAS = "my_alias"
MAX_FEE = 100

KEY = "TEST_KEY"
PRIVATE_KEY = "1234"
MOCK_TX_HASH = 1
TX_STATUS = TransactionStatus(MOCK_TX_HASH, TxStatus.ACCEPTED_ON_L2, None)


@pytest.mark.asyncio
@patch("nile_upgrades.deploy_proxy.declare_contract")
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
@patch("nile.core.types.account.Account.deploy_contract")
async def test_deploy_proxy(
    mock_deploy, mock_get_proxy_artifact_path, mock_get_selector, mock_declare_impl
):
    mock_declare_impl.side_effect = [CLASS_HASH, PROXY_CLASS_HASH]

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await deploy_proxy(NileRuntimeEnvironment(), account, CONTRACT, ARGS)

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, account, "initializer", PROXY_ARTIFACT_PATH, None, None)


@pytest.mark.asyncio
@patch("nile_upgrades.deploy_proxy.declare_contract")
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
@patch("nile.core.types.account.Account.deploy_contract")
async def test_deploy_proxy_all_opts(
    mock_deploy, mock_get_proxy_artifact_path, mock_get_selector, mock_declare_impl
):
    mock_declare_impl.side_effect = [CLASS_HASH, PROXY_CLASS_HASH]

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await deploy_proxy(NileRuntimeEnvironment(), account, CONTRACT, ARGS, CUSTOM_INIT, ALIAS, MAX_FEE)

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, account, CUSTOM_INIT, PROXY_ARTIFACT_PATH, ALIAS, MAX_FEE)


def _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, account, initializer, overriding_path, alias, max_fee):
    mock_declare_impl.assert_any_call(NETWORK, CONTRACT, account, max_fee)
    mock_declare_impl.assert_any_call(NETWORK, "Proxy", account, max_fee, overriding_path=overriding_path)

    mock_get_selector.assert_called_once_with(initializer)

    mock_deploy.assert_called_once_with(
        "Proxy",
        salt=123,
        unique=False,
        calldata=[CLASS_HASH, SELECTOR, len(ARGS), *ARGS],
        max_fee=max_fee,
        alias=alias,
        overriding_path=PROXY_ARTIFACT_PATH,
        abi=IMPL_ABI,
    )
