#!/usr/bin/env python3
"""Check Echo Contract Status"""

from algosdk.v2client import algod
from algosdk.logic import get_application_address
from beaker import client
from echo_contract import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def check_echo_status():
    APP_ID = int(input("Echo Contract APP_ID: "))
    app_addr = get_application_address(APP_ID)
    
    client_algod = algod.AlgodClient("", ALGOD_URL, "")
    
    # Check app balance
    try:
        info = client_algod.account_info(app_addr)
        balance = info["amount"] / 1_000_000
        
        print(f"🔄 Echo Contract Status")
        print(f"   APP_ID: {APP_ID}")
        print(f"   Address: {app_addr}")
        print(f"   Balance: {balance} ALGO")
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{app_addr}")
        
        # Try to read contract state
        try:
            app_info = client_algod.application_info(APP_ID)
            global_state = app_info.get("params", {}).get("global-state", [])
            
            total_received = 0
            last_sender = ""
            
            for item in global_state:
                key = item["key"]
                value = item["value"]
                
                if key == "dG90YWw=":  # "total" in base64
                    total_received = value["uint"] / 1_000_000
                elif key == "c2VuZGVy":  # "sender" in base64
                    last_sender = value.get("bytes", "")
            
            print(f"\n📊 Contract Stats:")
            print(f"   Total Received: {total_received} ALGO")
            if last_sender:
                print(f"   Last Sender: {last_sender}")
            
        except Exception as e:
            print(f"   Could not read state: {e}")
        
        print(f"\n💡 To Test:")
        print(f"   Send ALGO to: {app_addr}")
        print(f"   It will automatically bounce back!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_echo_status()