from scripts.helpful_scripts import get_account
from brownie import config, network, interface
from scripts.get_weth import get_weth
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_pool()
    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address,
                  erc20_address, account)
    print("Depositing...")
    tx = lending_pool.supply(erc20_address, amount,
                             account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited !")


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved !")
    return tx


def get_pool():
    pool_addresses_provider = interface.IPoolAddressesProvider(
        config["networks"][network.show_active()]["pool_addresses_provider"])
    pool_address = pool_addresses_provider.getPool()
    pool = interface.IPool(pool_address)
    return pool
