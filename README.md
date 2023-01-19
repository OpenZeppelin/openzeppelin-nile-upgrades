# OpenZeppelin Nile Upgrades

Plugin for [Nile](https://github.com/OpenZeppelin/nile) to deploy and manage [upgradeable contracts](https://docs.openzeppelin.com/contracts-cairo/proxies) on StarkNet.

> ## ⚠️ WARNING! ⚠️
>
> **This plugin does not currently validate contracts for upgrade safety.**
>
> This repo contains highly experimental code.
> Expect rapid iteration.
> **Use at your own risk.**

## Usage

Run the following functions from scripts with the `NileRuntimeEnvironment`.

### `deploy_proxy`

Deploy an upgradeable proxy for an implementation contract.

Returns a Nile Transaction instance representing the proxy deployment.

```
async def deploy_proxy(
    nre, account, contract_name, initializer_args, initializer='initializer', salt=0, alias=None, max_fee=None
):
```

- `nre` - the `NileRuntimeEnvironment` object.

- `account` - the Account to use.

- `contract_name` - the name of the implementation contract.

- `initializer_args` - array of arguments for the initializer function.

- `initializer` - initializer function name. Defaults to `'initializer'`.

- `salt` - Specify the salt for the proxy address generation. Defaults to `0`.

- `alias` - Unique identifier for your proxy. Defaults to `None`.

- `max_fee` - Maximum fee for the transaction. Defaults to `None`.

Example usage:
```
tx = await nre.deploy_proxy(nre, account, "my_contract_v1", ["arg for initializer"])
tx_status, proxy_address, abi = await tx.execute(watch_mode="track")
```

### `upgrade_proxy`  

Upgrade a proxy to a different implementation contract.

Returns a Nile Transaction instance representing the upgrade operation.

```
async def upgrade_proxy(
    nre, account, proxy_address_or_alias, contract_name, max_fee=None
):
```

- `nre` - the `NileRuntimeEnvironment` object.

- `signer` - private key alias for the Account to use.

- `proxy_address_or_alias` - the proxy address or alias.

- `contract_name` - the name of the implementation contract to upgrade to.

- `max_fee` - Maximum fee for the transaction. Defaults to `None`.

Example usage:
```
tx = await nre.upgrade_proxy(nre, account, proxy_address, "my_contract_v2")
tx_status = await tx.execute(watch_mode="track")
```

## Contribute

### Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone https://github.com/OpenZeppelin/nile
3. Clone this project.
4. From this project's root, setup venv and install dependencies:
```
python3 -m venv env
source env/bin/activate
poetry install
pip3 install -e <your_path_to_nile_repo_from_step_2>
pip3 install -e .
poetry run compile
```

### Testing

`poetry run pytest tests`
