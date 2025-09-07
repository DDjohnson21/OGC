#!/usr/bin/env python3
"""Check contract balance"""

from algosdk.v2client import algod
from algosdk.logic import get_application_address

ALGOD_URL = "https://testnet-api.algonode.cloud"

def check_balance():
    APP_ID = int(input("Contract APP_ID: "))
    app_addr = get_application_address(APP_ID)
    
    client = algod.AlgodClient("", ALGOD_URL, "")
    
    try:
        info = client.account_info(app_addr)
        balance = info["amount"] / 1_000_000
        
        print(f"💰 Contract Balance")
        print(f"   APP_ID: {APP_ID}")
        print(f"   Address: {app_addr}")
        print(f"   Balance: {balance} ALGO")
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{app_addr}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_balance()