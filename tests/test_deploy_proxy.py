"""Tests for deploy proxy."""
import logging
from unittest.mock import patch

from nile.nre import NileRuntimeEnvironment
from nile_upgrades.common import get_contract_abi

from nile_upgrades.deploy_proxy import deploy_proxy


NETWORK = "localhost"
CONTRACT = "contract"
SIGNER = "PKEY1"

SELECTOR = 1
CLASS_HASH = 16
ARGS = ["abc", 123]
PROXY_ADDR = "0x000000000000000000000000000000000000000000000000000000000000000f"
PROXY_ADDR_INT = 15
PROXY_ARTIFACT_PATH = ("upgrades/artifacts", "upgrades/artifacts/abis")
IMPL_ABI = get_contract_abi(CONTRACT)

CUSTOM_INIT = "my_init_func"
ALIAS = "my_alias"
MAX_FEE = 100


@patch("nile_upgrades.deploy_proxy.declare_impl", return_value=CLASS_HASH)
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile.nre.NileRuntimeEnvironment.deploy", return_value=(PROXY_ADDR_INT, IMPL_ABI))
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
def test_deploy_proxy(
    mock_get_proxy_artifact_path, mock_deploy, mock_get_selector, mock_declare_impl, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    result = deploy_proxy(NileRuntimeEnvironment(), SIGNER, CONTRACT, ARGS);
    assert result == PROXY_ADDR_INT

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, caplog, "initializer", None, None)


@patch("nile_upgrades.deploy_proxy.declare_impl", return_value=CLASS_HASH)
@patch("nile_upgrades.deploy_proxy.get_selector_from_name", return_value=SELECTOR)
@patch("nile.nre.NileRuntimeEnvironment.deploy", return_value=(PROXY_ADDR_INT, IMPL_ABI))
@patch("nile_upgrades.deploy_proxy._get_proxy_artifact_path", return_value=PROXY_ARTIFACT_PATH)
def test_deploy_proxy_all_opts(
    mock_get_proxy_artifact_path, mock_deploy, mock_get_selector, mock_declare_impl, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    result = deploy_proxy(NileRuntimeEnvironment(), SIGNER, CONTRACT, ARGS, CUSTOM_INIT, ALIAS, MAX_FEE);
    assert result == PROXY_ADDR_INT

    _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, caplog, CUSTOM_INIT, ALIAS, MAX_FEE)


def _assert_calls_and_logs(mock_deploy, mock_get_selector, mock_declare_impl, caplog, initializer, alias, max_fee):
    mock_declare_impl.assert_called_once_with(NETWORK, CONTRACT, SIGNER, max_fee)

    mock_get_selector.assert_called_once_with(initializer)

    mock_deploy.assert_called_once_with(
        "Proxy",
        arguments=[CLASS_HASH, SELECTOR, len(ARGS), *ARGS],
        alias=alias,
        overriding_path=PROXY_ARTIFACT_PATH,
        abi=IMPL_ABI,
    )

    # check logs
    assert f"Proxy deployed to address {PROXY_ADDR} using ABI {IMPL_ABI}" in caplog.text
