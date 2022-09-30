from nile_upgrades.deploy_proxy import deploy_proxy
from nile_upgrades.upgrade_proxy import upgrade_proxy

def test_callable():
    assert callable(deploy_proxy)
    assert callable(upgrade_proxy)

