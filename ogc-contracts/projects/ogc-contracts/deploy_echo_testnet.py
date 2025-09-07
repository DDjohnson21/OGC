#!/usr/bin/env python3
"""Deploy Echo Contract to TestNet"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from echo_contract import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def deploy_echo_contract():
    print("🔄 Deploying Echo Contract to TestNet")
    print("This contract automatically sends ALGO back when it receives it!")
    
    # Get deployer account
    mnemo = input("Enter your 25-word TestNet mnemonic: ").strip()
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
        
        print("Deploying Echo Contract...")
        app_id, app_addr, _ = app_client.create()
        
        print(f"\n✅ Echo Contract Deployed!")
        print(f"   APP_ID: {app_id}")
        print(f"   APP_ADDRESS: {app_addr}")
        print(f"   Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        # Fund the app for inner transactions (needs ALGO to send back)
        print(f"\nFunding contract with 2 ALGO for operations...")
        sp = algod_client.suggested_params()
        fund_txn = algosdk.transaction.PaymentTxn(addr, sp, app_addr, 2_000_000)
        stx = fund_txn.sign(sk)
        txid = algod_client.send_transaction(stx)
        algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ Contract funded")
        
        print(f"\n🎯 YOUR PERMANENT ECHO ADDRESS:")
        print(f"📍 {app_addr}")
        print(f"\n📱 How to Test:")
        print(f"1. Send ANY amount of ALGO to: {app_addr}")
        print(f"2. Contract will automatically send it back (minus 0.001 ALGO fee)")
        print(f"3. Check transactions on: https://testnet.algoexplorer.io/address/{app_addr}")
        
        print(f"\n🔍 Monitor Contract:")
        print(f"python check_echo_status.py")
        
        return app_id, app_addr
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None, None

if __name__ == "__main__":
    deploy_echo_contract()