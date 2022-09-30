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

Options:
  --initializer TEXT  Initializer function name. Defaults to 'initializer'
  --alias TEXT        Unique identifier for your proxy.
  --max_fee TEXT      Maximum fee for the transaction. Defaults to 0.
```

Example usage with `nre`:
```
proxy_address = nre.deploy_proxy(["MY_ACCOUNT_ALIAS", "my_contract_v1", "argument for initializer"])
```

### `upgrade_proxy`  

Upgrade a proxy to a different implementation contract.

```
nile upgrade_proxy [OPTIONS] SIGNER PROXY_ADDRESS_OR_ALIAS CONTRACT_NAME

Options:
  --max_fee TEXT  Maximum fee for the transaction. Defaults to 0.
  --help          Show this message and exit.
```

Example usage with `nre`:
```
tx_hash = nre.upgrade_proxy(["MY_ACCOUNT_ALIAS", proxy_address, "my_contract_v2"])
```

## Contribute

### Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies: `poetry install`

### Testing

`poetry run pytest tests`
