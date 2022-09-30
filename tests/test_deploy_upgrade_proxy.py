"""Tests for deploying and upgrading a proxy."""
import os
import shutil
import sys
from multiprocessing import Process
from os import getpid, kill
from pathlib import Path
from signal import SIGINT
from threading import Timer
from time import sleep
from unittest.mock import patch
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from click.testing import CliRunner

from nile.cli import cli
from nile.common import (
    ABIS_DIRECTORY,
    BUILD_DIRECTORY,
    CONTRACTS_DIRECTORY,
)

RESOURCES_DIR = Path(__file__).parent / "resources"


@pytest.fixture(autouse=True)
def tmp_working_dir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def create_process(target, args):
    """Spawns another process in Python."""
    p = Process(target=target, args=args)
    return p


def start_node(seconds, node_args):
    """Start node with host and port specified in node_args and life in seconds."""
    # Timed kill command with SIGINT to close Node process
    Timer(seconds, lambda: kill(getpid(), SIGINT)).start()
    CliRunner().invoke(cli, ["node", *node_args])


def check_node(p, seconds, gateway_url):
    """Check if node is running while spawned process is alive."""
    check_runs = 0
    while p.is_alive and check_runs < seconds:
        try:
            status = urlopen(gateway_url + "is_alive").getcode()
            return status
        except URLError:
            check_runs += 1
            sleep(1)
            continue


@patch.dict(os.environ, {"PKEY1": "1234"})
@pytest.mark.xfail(
    sys.version_info >= (3, 10),
    reason="Issue in cairo-lang. "
    "See https://github.com/starkware-libs/cairo-lang/issues/27",
)
def test_compile():
    contract_v1 = RESOURCES_DIR / "contracts" / "contract.cairo"
    contract_v2 = RESOURCES_DIR / "contracts" / "contract_v2.cairo"
    script = RESOURCES_DIR / "scripts" / "deploy_upgrade_proxy.py"

    target_dir = Path(CONTRACTS_DIRECTORY)
    target_dir.mkdir()

    shutil.copyfile(contract_v1, target_dir / "contract.cairo")
    shutil.copyfile(contract_v2, target_dir / "contract_v2.cairo")

    abi_dir = Path(ABIS_DIRECTORY)
    build_dir = Path(BUILD_DIRECTORY)

    # Compile contracts
    result = CliRunner().invoke(cli, ["compile"])
    assert result.exit_code == 0

    assert {f.name for f in abi_dir.glob("*.json")} == {"contract.json", "contract_v2.json"}
    assert {f.name for f in build_dir.glob("*.json")} == {"contract.json", "contract_v2.json"}

    # Start node
    p = spawn_gateway()

    # Run test script
    result = CliRunner().invoke(cli, ["run", str(script)])
    assert result.exit_code == 0

    # Check script output
    assert "balance from v1: ['1']" in result.output
    assert "balance from v2: ['1']" in result.output
    assert "balance after reset from v2: ['0']" in result.output

    p.terminate()


def spawn_gateway():
    # TODO this currently requires starknet-devnet==0.3.1 and openzeppelin-cairo-contracts==0.4.0b to be manually installed

    # Node timeout
    seconds = 60

    # Spawn process to start StarkNet local network with specified port
    # i.e. $ nile node --host localhost --port 5000
    p = create_process(target=start_node, args=(seconds, [ "--host", "localhost", "--port", "5000" ]))
    p.start()

    # Check node heartbeat and assert that it is running
    status = check_node(p, seconds, "http://127.0.0.1:5000/")
    assert status == 200

    return p
