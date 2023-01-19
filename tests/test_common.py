"""Tests for common."""
import logging
import os
import pytest
from unittest.mock import patch

from nile.core.types.tx_wrappers import DeclareTxWrapper
from nile.utils.status import TransactionStatus, TxStatus

from nile_upgrades.common import declare_class, get_contract_abi

from mocks.mock_account import MockAccount


NETWORK = "localhost"
CONTRACT = "contract"

CLASS_HASH = 16
PADDED_HASH = "0x000000000000000000000000000000000000000000000000000000000000010"
WRONG_HASH = "0x000000000000000000000000000000000000000000000000000000000000011"

KEY = "TEST_KEY"
PRIVATE_KEY = "1234"
MOCK_TX_HASH = 1
TX_STATUS_ACCEPTED = TransactionStatus(MOCK_TX_HASH, TxStatus.ACCEPTED_ON_L2, None)
TX_STATUS_REJECTED = TransactionStatus(MOCK_TX_HASH, TxStatus.REJECTED, None)


@pytest.mark.asyncio
@patch("nile_upgrades.common.get_class_hash", return_value=CLASS_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=True)
async def test_declare_class_already_exists(
    mock_class_hash_exists, mock_get_hash, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    result = await declare_class(NETWORK, CONTRACT, account, None)
    assert result == CLASS_HASH

    # check logs
    assert f"Contract class with hash {PADDED_HASH} already exists" in caplog.text


@pytest.mark.asyncio
@patch("nile_upgrades.common.get_class_hash", return_value=CLASS_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=False)
@patch("nile.core.types.account.Account.declare", return_value=DeclareTxWrapper(None, None))
@patch(
    "nile.core.types.tx_wrappers.DeclareTxWrapper.execute",
    return_value=(TX_STATUS_ACCEPTED, WRONG_HASH),
)
async def test_declare_class_hash_not_match(
    mock_execute, mock_declare, mock_class_hash_exists, mock_get_hash, caplog
):
    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    with pytest.raises(Exception) as e:
        await declare_class(NETWORK, CONTRACT, account, None)
    assert f"Declared hash {WRONG_HASH} does not match expected hash {PADDED_HASH}" in str(e.value)


@pytest.mark.asyncio
@patch("nile_upgrades.common.get_class_hash", return_value=CLASS_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=False)
@patch("nile.core.types.account.Account.declare", return_value=DeclareTxWrapper(None, None))
@patch(
    "nile.core.types.tx_wrappers.DeclareTxWrapper.execute",
    return_value=(TX_STATUS_REJECTED, PADDED_HASH),
)
async def test_declare_class_rejected(
    mock_execute, mock_declare, mock_class_hash_exists, mock_get_hash, caplog
):
    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    with pytest.raises(Exception) as e:
        await declare_class(NETWORK, CONTRACT, account, None)
    assert f"Could not declare contract class. Transaction rejected." in str(e.value)


@pytest.mark.asyncio
@patch("nile_upgrades.common.get_class_hash", return_value=CLASS_HASH)
@patch("nile_upgrades.common.class_hash_exists", return_value=False)
@patch("nile.core.types.account.Account.declare", return_value=DeclareTxWrapper(None, None))
@patch(
    "nile.core.types.tx_wrappers.DeclareTxWrapper.execute",
    return_value=(TX_STATUS_ACCEPTED, PADDED_HASH),
)
async def test_declare_class(
    mock_execute, mock_declare, mock_class_hash_exists, mock_get_hash, caplog
):
    logging.getLogger().setLevel(logging.DEBUG)

    with patch.dict(os.environ, {KEY: PRIVATE_KEY}, clear=False):
        account = await MockAccount(KEY, NETWORK)

    result = await declare_class(NETWORK, CONTRACT, account, None)
    assert result == CLASS_HASH

    # check logs
    assert f"Contract class declared with hash {PADDED_HASH}" in caplog.text


def test_get_contract_abi():
    result = get_contract_abi("mycontract")
    assert result == f"artifacts/abis/mycontract.json"
