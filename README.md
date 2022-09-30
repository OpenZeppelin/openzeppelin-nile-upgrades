# OpenZeppelin Nile Upgrades

Plugin for [Nile](https://github.com/OpenZeppelin/nile) to deploy and manage upgradeable contracts on StarkNet.

> ## ⚠️ WARNING! ⚠️
>
> This repo contains highly experimental code.
> Expect rapid iteration.
> **Use at your own risk.**

## Usage

### `deploy_proxy`
Deploy an upgradeable proxy for an implementation contract.

```
nile deploy_proxy [OPTIONS] SIGNER CONTRACT_NAME [INITIALIZER_ARGS]...

SIGNER - private key alias for the Account to use.

CONTRACT_NAME - the name of the implementation contract.
    
INITIALIZER_ARGS - arguments for the initializer function.

Options:
  --initializer TEXT  Initializer function name. Defaults to 'initializer'
  --alias TEXT        Unique identifier for your proxy.
  --max_fee TEXT      Maximum fee for the transaction. Defaults to 0.
```

Example usage with `nre`:
```
proxy_address = nre.deploy_proxy(["PKEY1", "my_contract_v1", "arg for initializer"])
```

### `upgrade_proxy`  

Upgrade a proxy to a different implementation contract.

```
nile upgrade_proxy [OPTIONS] SIGNER PROXY_ADDRESS_OR_ALIAS CONTRACT_NAME

SIGNER - private key alias for the Account to use.

PROXY_ADDRESS_OR_ALIAS - the proxy address or alias.

CONTRACT_NAME - the name of the implementation contract to upgrade to.

Options:
  --max_fee TEXT  Maximum fee for the transaction. Defaults to 0.
  --help          Show this message and exit.
```

Example usage with `nre`:
```
tx_hash = nre.upgrade_proxy(["PKEY1", proxy_address, "my_contract_v2"])
```

## Contribute

### Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone https://github.com/ericglau/nile with branch `upgrades`, e.g.:
```
git clone https://github.com/ericglau/nile -b upgrades nile_fork
```
3. Clone this project.
4. From this project's root, setup venv and install dependencies:
```
python3 -m venv env
source env/bin/activate
poetry install
pip3 install cairo-lang==0.10.0
pip3 install openzeppelin-cairo-contracts==0.4.0b
pip3 install -e <your_path_to_nile_fork_from_step_2>
pip3 install -e .
```

### Testing

`poetry run pytest tests`
