from nile.utils import hex_address

async def run(nre):
    accounts = await nre.get_accounts(predeployed=True)
    declarer_account = accounts[0]

    tx = await nre.deploy_proxy(nre, declarer_account, "contract", [declarer_account.address])
    _, proxy, abi = await tx.execute(watch_mode="track")
    print(f"Proxy deployed to address {hex_address(proxy)} using ABI {abi}")

    tx = await declarer_account.send(proxy, "increase_balance", calldata=['1'])
    await tx.execute(watch_mode="track")
    print(f"balance from v1: {await nre.call(proxy, 'get_balance')}")

    tx = await nre.upgrade_proxy(nre, declarer_account, proxy, "contract_v2")
    await tx.execute(watch_mode="track")
    print(f"balance from v2: {await nre.call(proxy, 'get_balance')}")

    tx = await declarer_account.send(proxy, "reset_balance", calldata=[])
    await tx.execute(watch_mode="track")
    print(f"balance after reset from v2: {await nre.call(proxy, 'get_balance')}")
