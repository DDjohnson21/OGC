#!/usr/bin/env python3
"""Deploy Sender Contract to TestNet"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from sender_contract import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def deploy_sender():
    print("📤 Deploying ALGO Sender Contract to TestNet")
    
    # Load from environment
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    mnemo = os.getenv('TESTNET_MNEMONIC')
    if not mnemo:
        print("❌ TESTNET_MNEMONIC not found in .env file")
        return
    
    try:
        sk = mnemonic.to_private_key(mnemo)
        addr = algosdk.account.address_from_private_key(sk)
        print(f"Deploying from: {addr}")
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        return
    
    # Connect to TestNet
    algod_client = algod.AlgodClient("", ALGOD_URL, "")
    
    # Check balance
    try:
        info = algod_client.account_info(addr)
        balance = info["amount"] / 1_000_000
        print(f"Account balance: {balance} ALGO")
        
        if balance < 1.0:
            print("❌ Need at least 1 ALGO for deployment and funding")
            print("Get TestNet ALGO from: https://testnet.algoexplorer.io/dispenser")
            print(f"Your address: {addr}")
            return
    except Exception as e:
        print(f"❌ Could not check balance: {e}")
        return
    
    try:
        # Create signer
        signer = algosdk.atomic_transaction_composer.AccountTransactionSigner(sk)
        
        # Deploy
        app_client = client.ApplicationClient(
            client=algod_client,
            app=app,
            signer=signer,
        )
        
        print("Deploying Sender Contract...")
        app_id, app_addr, _ = app_client.create()
        
        print(f"\n✅ Sender Contract Deployed!")
        print(f"   APP_ID: {app_id}")
        print(f"   APP_ADDRESS: {app_addr}")
        print(f"   Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        # Fund the contract so it can send ALGO
        print(f"\nFunding contract with 5 ALGO...")
        sp = algod_client.suggested_params()
        fund_txn = algosdk.transaction.PaymentTxn(addr, sp, app_addr, 5_000_000)
        stx = fund_txn.sign(sk)
        txid = algod_client.send_transaction(stx)
        algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ Contract funded with 5 ALGO")
        
        print(f"\n🎯 CONTRACT CAN NOW SEND ALGO!")
        print(f"   Use: python send_from_contract.py")
        print(f"   APP_ID: {app_id}")
        
        return app_id, app_addr
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None, None

if __name__ == "__main__":
    deploy_sender()