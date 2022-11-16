"""Tests for common."""
import logging
from unittest.mock import patch

from nile_upgrades.common import declare_impl, get_contract_abi


NETWORK = "localhost"
CONTRACT = "contract"
SIGNER = "PKEY1"

CLASS_HASH = 16
PADDED_HASH = "0x000000000000000000000000000000000000000000000000000000000000010"
WRONG_HASH = "0x000000000000000000000000000000000000000000000000000000000000011"


@patch("nile_upgrades.common.get_hash", return_value=PADDED_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=True)
def test_declare_impl_already_exists(
    mock_class_hash_exists, mock_get_hash, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    result = declare_impl(NETWORK, CONTRACT, SIGNER, None);
    assert result == CLASS_HASH

    # check logs
    assert f"Implementation with hash {PADDED_HASH} already exists" in caplog.text


@patch("nile_upgrades.common.get_hash", return_value=PADDED_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=False)
@patch("nile.core.account.Account.declare", return_value=WRONG_HASH)
def test_declare_impl_not_match(
    mock_declare, mock_class_hash_exists, mock_get_hash, caplog
):
    try:
        declare_impl(NETWORK, CONTRACT, SIGNER, None);
        raise AssertionError("declare_impl expected to fail due to mismatched class hash")
    except Exception as e:
        assert f"Declared hash {WRONG_HASH} does not match expected hash {PADDED_HASH}" in str(e)


@patch("nile_upgrades.common.get_hash", return_value=PADDED_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=False)
@patch("nile.core.account.Account.declare", return_value=PADDED_HASH)
def test_declare_impl(
    mock_declare, mock_class_hash_exists, mock_get_hash, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    result = declare_impl(NETWORK, CONTRACT, SIGNER, None);
    assert result == CLASS_HASH

    # check logs
    assert f"Implementation declared with hash {PADDED_HASH}" in caplog.text


def test_get_contract_abi():
    result = get_contract_abi("mycontract")
    assert result == f"artifacts/abis/mycontract.json"