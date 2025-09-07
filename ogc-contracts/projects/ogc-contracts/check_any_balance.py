#!/usr/bin/env python3
"""Check balance of any address or contract"""

from algosdk.v2client import algod
from algosdk.logic import get_application_address

ALGOD_URL = "https://testnet-api.algonode.cloud"

def check_any_balance():
    print("💰 Check Balance")
    print("1. Check wallet address")
    print("2. Check contract (APP_ID)")
    
    choice = input("Choose (1 or 2): ").strip()
    
    client = algod.AlgodClient("", ALGOD_URL, "")
    
    if choice == "1":
        # Check wallet address
        address = input("Paste wallet address: ").strip()
        try:
            info = client.account_info(address)
            balance = info["amount"] / 1_000_000
            
            print(f"\n💰 Wallet Balance")
            print(f"   Address: {address}")
            print(f"   Balance: {balance} ALGO")
            print(f"   Explorer: https://testnet.algoexplorer.io/address/{address}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif choice == "2":
        # Check contract
        app_id = int(input("Contract APP_ID: "))
        app_addr = get_application_address(app_id)
        
        try:
            info = client.account_info(app_addr)
            balance = info["amount"] / 1_000_000
            
            print(f"\n💰 Contract Balance")
            print(f"   APP_ID: {app_id}")
            print(f"   Address: {app_addr}")
            print(f"   Balance: {balance} ALGO")
            print(f"   Explorer: https://testnet.algoexplorer.io/address/{app_addr}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    check_any_balance()