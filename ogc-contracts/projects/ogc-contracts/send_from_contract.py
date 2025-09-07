#!/usr/bin/env python3
"""Send ALGO from contract to any wallet"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from sender_contract import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def send_from_contract():
    print("📤 Send ALGO from Contract to Wallet")
    
    # Load contract owner mnemonic from environment
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mnemo = os.getenv('TESTNET_MNEMONIC')
    if not mnemo:
        print("❌ TESTNET_MNEMONIC not found in .env file")
        return
    
    APP_ID = int(input("Sender Contract APP_ID: "))
    recipient = input("Recipient wallet address: ").strip()
    amount_algo = float(input("Amount to send (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    try:
        sk = mnemonic.to_private_key(mnemo)
        addr = algosdk.account.address_from_private_key(sk)
        
        # Connect to TestNet
        algod_client = algod.AlgodClient("", ALGOD_URL, "")
        
        # Create app client
        signer = algosdk.atomic_transaction_composer.AccountTransactionSigner(sk)
        app_client = client.ApplicationClient(
            client=algod_client,
            app=app,
            app_id=APP_ID,
            signer=signer,
        )
        
        print(f"\n📤 Sending {amount_algo} ALGO to {recipient}...")
        
        # Call send_algo method
        app_client.call("send_algo", recipient=recipient, amount=amount_micro)
        
        print(f"✅ SUCCESS! Sent {amount_algo} ALGO from contract!")
        print(f"   To: {recipient}")
        print(f"   Check: https://testnet.algoexplorer.io/address/{recipient}")
        
        # Check contract balance
        balance = app_client.call("get_balance").return_value
        total_sent = app_client.call("get_total_sent").return_value
        
        print(f"\n📊 Contract Status:")
        print(f"   Remaining balance: {balance/1_000_000} ALGO")
        print(f"   Total sent: {total_sent/1_000_000} ALGO")
        
    except Exception as e:
        print(f"❌ Send failed: {e}")

if __name__ == "__main__":
    send_from_contract()