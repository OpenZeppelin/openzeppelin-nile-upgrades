"""Tests Proxy artifact was compiled."""
import os
from pathlib import Path


def test_proxy_compiled():
    project_root = os.path.dirname(Path(__file__).parent)
    proxy_artifact = f"{project_root}/src/nile_upgrades/artifacts/Proxy.json"
    assert Path(proxy_artifact).absolute().is_file(), "Compile proxy contract with: poetry run compile"
