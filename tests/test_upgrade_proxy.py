"""Tests for deploy proxy."""
import logging
from unittest.mock import patch

import pytest

from nile.nre import NileRuntimeEnvironment
from nile_upgrades.common import get_contract_abi

from nile_upgrades.upgrade_proxy import _get_tx_hash, _load_deployment, upgrade_proxy


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


@patch("nile_upgrades.upgrade_proxy._load_deployment", return_value=PROXY_ADDR_INT)
@patch("nile_upgrades.upgrade_proxy.declare_impl", return_value=CLASS_HASH)
@patch("nile.core.account.Account.send", return_value=f"Transaction hash: {TX_HASH}")
@patch("nile.deployments.update_abi")
def test_upgrade_proxy(
    mock_update_abi, mock_send, mock_declare_impl, mock_load_deployment, caplog
):
    logging.getLogger().setLevel(logging.INFO)

    upgrade_proxy(NileRuntimeEnvironment(), SIGNER, PROXY_ADDR, CONTRACT)

    _assert_calls_and_logs(mock_update_abi, mock_send, caplog, None)


@patch("nile_upgrades.upgrade_proxy._load_deployment", return_value=PROXY_ADDR_INT)
@patch("nile_upgrades.upgrade_proxy.declare_impl", return_value=CLASS_HASH)
@patch("nile.core.account.Account.send", return_value=f"Transaction hash: {TX_HASH}")
@patch("nile.deployments.update_abi")
def test_upgrade_proxy_all_opts(
    mock_update_abi, mock_send, mock_declare_impl, mock_load_deployment, caplog
):
    logging.getLogger().setLevel(logging.INFO)

    upgrade_proxy(NileRuntimeEnvironment(), SIGNER, PROXY_ADDR, CONTRACT, MAX_FEE)

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
    assert f"Upgrade transaction hash: {TX_HASH}" in caplog.text


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


def test_get_tx_hash():
    result = _get_tx_hash(
        """Something: 0x001
        Transaction hash: 0x002
        Something else: 123
        """)
    assert result == "0x002"
