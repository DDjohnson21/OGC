#!/usr/bin/env python3
"""Check app balance on TestNet"""

from algosdk.v2client import algod
from algosdk.logic import get_application_address

ALGOD_URL = "https://testnet-api.algonode.cloud"

APP_ID = int(input("APP_ID: "))
app_addr = get_application_address(APP_ID)

client = algod.AlgodClient("", ALGOD_URL, "")
info = client.account_info(app_addr)

print(f"APP_ADDRESS: {app_addr}")
print(f"Balance: {info['amount']/1_000_000} ALGO ({info['amount']} microALGO)")
print(f"Explorer: https://testnet.algoexplorer.io/address/{app_addr}")

# Check if it's an app account
if info.get("apps-total-schema"):
    print("✅ This is an application account")
else:
    print("⚠️  This might not be an app account")