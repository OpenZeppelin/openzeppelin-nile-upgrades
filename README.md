# OpenZeppelin Nile Upgrades

Plugin for [Nile](https://github.com/OpenZeppelin/nile) to deploy and manage [upgradeable smart contracts](https://docs.openzeppelin.com/contracts-cairo/proxies) on StarkNet.

> ## ⚠️ WARNING! ⚠️
>
> This plugin does not currently validate contracts for upgrade safety (see [issue 34](https://github.com/OpenZeppelin/openzeppelin-nile-upgrades/issues/34)).
**Review your contracts for upgrade safety before performing any deployments or upgrades.**

> ## ⚠️ WARNING! ⚠️
>
> This repo contains highly experimental code.
> Expect rapid iteration.
> **Use at your own risk.**

## Installation

```
pip install nile-upgrades
```

## Usage

Run the following functions from scripts with the `NileRuntimeEnvironment`.

### `deploy_proxy`

Deploy an upgradeable proxy for an implementation contract.

Returns a Nile Transaction instance representing the proxy deployment.

```
async def deploy_proxy(
    nre,
    account,
    contract_name,
    initializer_args,
    initializer='initializer',
    salt=0,
    unique=True,
    alias=None,
    max_fee_declare_impl=None,
    max_fee_declare_proxy=None,
    max_fee_deploy_proxy=None,
)
```

- `nre` - the `NileRuntimeEnvironment` object.

- `account` - the Account to use.

- `contract_name` - the name of the implementation contract.

- `initializer_args` - array of arguments for the initializer function.

- `initializer` - initializer function name. Defaults to `'initializer'`.

- `salt` - the salt for proxy address generation. Defaults to `0`.

- `unique` - whether the account address should be taken into account for proxy address generation. Defaults to `True`.

- `alias` - Unique identifier for your proxy. Defaults to `None`.

- `max_fee_declare_impl` - Maximum fee for declaring the implementation contract. Defaults to `None`.

- `max_fee_declare_proxy` - Maximum fee for declaring the proxy contract. Defaults to `None`.

- `max_fee_deploy_proxy` - Maximum fee for deploying the proxy contract. Defaults to `None`.

Example usage:
```
tx = await nre.deploy_proxy(nre, account, "my_contract_v1", 123, True, ["arg for initializer"])
tx_status, proxy_address, abi = await tx.execute(watch_mode="track")
```

### `upgrade_proxy`  

Upgrade a proxy to a different implementation contract.

Returns a Nile Transaction instance representing the upgrade operation.

```
async def upgrade_proxy(
    nre,
    account,
    proxy_address_or_alias,
    contract_name,
    max_fee_declare_impl=None,
    max_fee_upgrade_proxy=None,
)
```

- `nre` - the `NileRuntimeEnvironment` object.

- `account` - the Account to use.

- `proxy_address_or_alias` - the proxy address or alias.

- `contract_name` - the name of the implementation contract to upgrade to.

- `max_fee_declare_impl` - Maximum fee for declaring the new implementation contract. Defaults to `None`.

- `max_fee_upgrade_proxy` - Maximum fee for upgrading the proxy to the new implementation. Defaults to `None`.

Example usage:
```
tx = await nre.upgrade_proxy(nre, account, proxy_address, "my_contract_v2")
tx_status = await tx.execute(watch_mode="track")
```

## Contribute

### Setup

#### Using the latest Nile release supported by this plugin

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone this project.
3. From this project's root, create a virtualenv, activate it, and install dependencies:
```
python3.9 -m venv env
source env/bin/activate
pip install -U pip setuptools
poetry install
pip install -e .
poetry run compile
```

**or**

#### Using current Nile source code

1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Clone https://github.com/OpenZeppelin/nile
3. Clone this project.
4. From this project's root, create a virtualenv, activate it, and install dependencies:
```
python3.9 -m venv env
source env/bin/activate
pip install -U pip setuptools
poetry install
pip install -e <your_path_to_nile_repo_from_step_2>
pip install -e .
poetry run compile
```

### Testing

`poetry run pytest tests`
