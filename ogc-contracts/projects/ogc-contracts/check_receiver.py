#!/usr/bin/env python3
"""Check Simple Receiver Status"""

from algosdk.v2client import algod
from algosdk.logic import get_application_address

ALGOD_URL = "https://testnet-api.algonode.cloud"

def check_receiver():
    APP_ID = int(input("Receiver APP_ID: "))
    app_addr = get_application_address(APP_ID)
    
    client = algod.AlgodClient("", ALGOD_URL, "")
    
    try:
        # Check app balance
        info = client.account_info(app_addr)
        balance = info["amount"] / 1_000_000
        
        print(f"📥 Simple Receiver Status")
        print(f"   APP_ID: {APP_ID}")
        print(f"   Address: {app_addr}")
        print(f"   Balance: {balance} ALGO")
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{app_addr}")
        
        # Check recent transactions
        print(f"\n🔍 Recent Activity:")
        print(f"   View all transactions: https://testnet.algoexplorer.io/address/{app_addr}")
        
        if balance > 0:
            print(f"✅ SUCCESS! Contract has received {balance} ALGO")
        else:
            print(f"⏳ No ALGO received yet")
            print(f"   Send ALGO to: {app_addr}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_receiver()