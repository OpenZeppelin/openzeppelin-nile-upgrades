from nile.core.account import Account

async def run(nre):
    signer = "PKEY1"
    account = await Account(signer, nre.network)

    proxy = await nre.deploy_proxy(nre, signer, "contract", [account.address])

    await account.send(proxy, "increase_balance", calldata=['1'])
    print(f"balance from v1: {await nre.call(proxy, 'get_balance')}")

    tx = await nre.upgrade_proxy(nre, signer, proxy, "contract_v2")
    print(f"upgrade tx: {tx}")
    print(f"balance from v2: {await nre.call(proxy, 'get_balance')}")

    await account.send(proxy, "reset_balance", calldata=[])
    print(f"balance after reset from v2: {await nre.call(proxy, 'get_balance')}")
