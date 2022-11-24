"""Command to compile Proxy contract."""
import os
import subprocess
import logging
import inspect
from pathlib import Path

import openzeppelin


def main():
    contracts = getContractsDir()
    proxy_contract = getProxyContract(contracts)
    cairo_path = Path(contracts).parent.absolute()
    output_file = prepareOutputFile()

    cmd = f"""
    starknet-compile {proxy_contract} \
        --cairo_path={cairo_path}
        --output {output_file}
    """

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    process.communicate()

    if (process.returncode != 0):
        raise Exception(f"Failed to compile proxy: {process.stderr}")
    else:
        logging.info(f"Compiled proxy to {output_file}")


def getContractsDir():
    contracts_dir = os.path.dirname(inspect.getfile(openzeppelin))
    logging.debug(f"Found openzeppelin-cairo-contracts at {contracts_dir}")
    return contracts_dir


def getProxyContract(contracts_dir):
    proxy_contract = f"{contracts_dir}/upgrades/presets/Proxy.cairo"
    if not Path(proxy_contract).is_file():
        raise Exception(f"Proxy contract not found at {proxy_contract}")
    return proxy_contract


def prepareOutputFile():
    output_dir = "src/nile_upgrades/artifacts"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_file = f"{output_dir}/Proxy.json"
    Path(output_file).unlink(missing_ok=True)
    return output_file
