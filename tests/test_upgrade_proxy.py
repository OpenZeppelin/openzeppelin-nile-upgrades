"""Tests for deploy proxy."""
import logging
import os
import pytest
from unittest.mock import patch

from nile.nre import NileRuntimeEnvironment
from nile.utils.status import TransactionStatus, TxStatus

from nile_upgrades.common import get_contract_abi
from nile_upgrades.upgrade_proxy import _load_deployment, upgrade_proxy

from mocks.mock_account import MockAccount


NETWORK = "localhost"
CONTRACT = "contract"
SIGNER = "PKEY1"

SELECTOR = 1
CLASS_HASH = 16
HEX_CLASS_HASH = "0x000000000000000000000000000000000000000000000000000000000000010"

PROXY_ADDR = "0x000000000000000000000000000000000000000000000000000000000000000f"
PROXY_ADDR_INT = 15
IMPL_ABI = get_contract_abi(CONTRACT)

ALIAS = "my_proxy"
MAX_FEE = 100

TX_HASH = "0xA"

KEY = "TEST_KEY"
PRIVATE_KEY = "1234"
MOCK_TX_HASH = 1
TX_STATUS = TransactionStatus(MOCK_TX_HASH, TxStatus.ACCEPTED_ON_L2, None)


@pytest.mark.asyncio
@patch("nile_upgrades.upgrade_proxy._load_deployment", return_value=PROXY_ADDR_INT)
@patch("nile_upgrades.upgrade_proxy.declare_contract", return_value=CLASS_HASH)
@patch("nile.core.types.account.Account.send")
@patch("nile.deployments.update_abi")
async def test_upgrade_proxy(
    mock_update_abi, mock_send, mock_declare_class, mock_load_deployment, caplog
):
    logging.getLogger().setLevel(logging.INFO)

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await upgrade_proxy(NileRuntimeEnvironment(), account, PROXY_ADDR, CONTRACT)

    _assert_calls_and_logs(mock_update_abi, mock_send, caplog, None)


@pytest.mark.asyncio
@patch("nile_upgrades.upgrade_proxy._load_deployment", return_value=PROXY_ADDR_INT)
@patch("nile_upgrades.upgrade_proxy.declare_contract", return_value=CLASS_HASH)
@patch("nile.core.types.account.Account.send")
@patch("nile.deployments.update_abi")
async def test_upgrade_proxy_all_opts(
    mock_update_abi, mock_send, mock_declare_class, mock_load_deployment, caplog
):
    logging.getLogger().setLevel(logging.INFO)

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    await upgrade_proxy(NileRuntimeEnvironment(), account, PROXY_ADDR, CONTRACT, MAX_FEE)

    _assert_calls_and_logs(mock_update_abi, mock_send, caplog, MAX_FEE)


def _assert_calls_and_logs(mock_update_abi, mock_send, caplog, max_fee):
    mock_send.assert_called_once_with(
        PROXY_ADDR_INT, "upgrade", calldata=[CLASS_HASH], max_fee=max_fee
    )

    mock_update_abi.assert_called_once_with(
        PROXY_ADDR_INT, IMPL_ABI, NETWORK
    )

    # check logs
    assert f"Upgrading proxy {PROXY_ADDR} to class hash {HEX_CLASS_HASH}" in caplog.text


@patch("nile.deployments.load", return_value=iter([(PROXY_ADDR_INT, IMPL_ABI)]))
def test_load_deployment(
    mock_load
):
    result = _load_deployment(PROXY_ADDR_INT, NETWORK)
    assert result == PROXY_ADDR_INT


@pytest.mark.parametrize(
    "identifier, exp_identifier",
    [
        (ALIAS, ALIAS),
        (PROXY_ADDR_INT, PROXY_ADDR)
    ]
)
@patch("nile.deployments.load", return_value=iter([]))
def test_load_deployment_not_found(
    mock_load, identifier, exp_identifier
):
    with pytest.raises(Exception) as e:
        _load_deployment(identifier, NETWORK)
    assert f"Deployment with address or alias {exp_identifier} not found" in str(e.value)


@patch("nile.deployments.load", return_value=iter([(PROXY_ADDR_INT, IMPL_ABI), (PROXY_ADDR_INT, IMPL_ABI)]))
def test_load_deployment_multiple_address(
    mock_load
):
    with pytest.raises(Exception) as e:
        _load_deployment(PROXY_ADDR_INT, NETWORK)
    assert f"Multiple deployments found with address or alias {PROXY_ADDR}" in str(e.value)


@patch("nile.deployments.load", return_value=iter([(PROXY_ADDR_INT, IMPL_ABI), (PROXY_ADDR_INT, IMPL_ABI)]))
def test_load_deployment_multiple_alias(
    mock_load
):
    with pytest.raises(Exception) as e:
        _load_deployment(ALIAS, NETWORK)
    assert f"Multiple deployments found with address or alias {ALIAS}" in str(e.value)
