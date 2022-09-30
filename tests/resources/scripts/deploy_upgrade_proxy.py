
from nile.core.account import Account

def run(nre):
    signer = "PKEY1"
    account = Account(signer, nre.network)

    proxy = nre.deploy_proxy([signer, "contract", account.address])

    account.send(proxy, "increase_balance", calldata=['1'])
    print(f"balance from v1: {nre.call(proxy, 'get_balance')}")

    tx = nre.upgrade_proxy([signer, proxy, "contract_v2"])
    print(f"upgrade tx: {tx}")
    print(f"balance from v2: {nre.call(proxy, 'get_balance')}")

    account.send(proxy, "reset_balance", calldata=[])
    print(f"balance after reset from v2: {nre.call(proxy, 'get_balance')}")
