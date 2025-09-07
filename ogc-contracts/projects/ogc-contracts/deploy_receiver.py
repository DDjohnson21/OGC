#!/usr/bin/env python3
"""Deploy Simple Receiver to TestNet"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from simple_receiver import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def deploy_receiver():
    print("📥 Deploying Simple ALGO Receiver to TestNet")
    
    # Get deployer account
    mnemo = input("Enter your mnemonic (24 or 25 words): ").strip()
    
    # Count words
    words = mnemo.split()
    print(f"Found {len(words)} words")
    
    if len(words) == 24:
        print("⚠️  You have 24 words, but Algorand needs 25")
        print("Check Pera Wallet again - there might be one more word")
        return
    elif len(words) != 25:
        print(f"❌ Expected 25 words, got {len(words)}")
        return
    
    try:
        sk = mnemonic.to_private_key(mnemo)
        addr = algosdk.account.address_from_private_key(sk)
        print(f"✅ Valid mnemonic")
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
        
        if balance < 0.5:
            print("❌ Need at least 0.5 ALGO for deployment")
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
        
        print("Deploying Simple Receiver...")
        app_id, app_addr, _ = app_client.create()
        
        print(f"\n✅ Simple Receiver Deployed!")
        print(f"   APP_ID: {app_id}")
        print(f"   APP_ADDRESS: {app_addr}")
        print(f"   Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        print(f"\n🎯 YOUR PERMANENT RECEIVER ADDRESS:")
        print(f"📍 {app_addr}")
        
        print(f"\n📱 How to Send ALGO:")
        print(f"1. Open Pera Wallet → TestNet")
        print(f"2. Send ANY amount to: {app_addr}")
        print(f"3. Contract will receive and log it")
        print(f"4. Check status: python check_receiver.py")
        
        return app_id, app_addr
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None, None

if __name__ == "__main__":
    deploy_receiver()