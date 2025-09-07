#!/usr/bin/env python3
"""Call release function on TestNet"""

import algosdk
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future import transaction as tx

ALGOD_URL = "https://testnet-api.algonode.cloud"

APP_ID = int(input("APP_ID: "))
mnemo = input("24-word TestNet mnemonic: ").strip()

try:
    sk = mnemonic.to_private_key(mnemo)
    addr = algosdk.account.address_from_private_key(sk)
    print(f"Calling from: {addr}")
    
    client = algod.AlgodClient("", ALGOD_URL, "")
    sp = client.suggested_params()
    
    # Call release method
    app_args = [b"release"]
    txn = tx.ApplicationNoOpTxn(addr, sp, APP_ID, app_args=app_args)
    stx = txn.sign(sk)
    txid = client.send_transaction(stx)
    
    print(f"Transaction sent: {txid}")
    print("Waiting for confirmation...")
    
    algosdk.transaction.wait_for_confirmation(client, txid, 4)
    print("✅ Release called successfully!")
    print(f"Explorer: https://testnet.algoexplorer.io/tx/{txid}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure:")
    print("- APP_ID is correct")
    print("- Mnemonic is valid TestNet account")
    print("- Account has some ALGO for fees")
    print("- Deadline has passed and goal was met")