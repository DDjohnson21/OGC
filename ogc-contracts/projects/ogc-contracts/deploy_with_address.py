#!/usr/bin/env python3
"""Deploy OGC Vault to TestNet with provided address"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from working_vault import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"
YOUR_ADDRESS = "SXIEIE2D7FOKUNQXUFUZIRYKE75RYD5KBN5BOYZFXLIL7LOTFX4VK3U7CE"

def deploy_to_testnet():
    print("🚀 Deploying OGC Vault to TestNet")
    print(f"Using address: {YOUR_ADDRESS}")
    
    # Get private key
    mnemo = input("Enter your 25-word mnemonic for this address: ").strip()
    try:
        sk = mnemonic.to_private_key(mnemo)
        addr = algosdk.account.address_from_private_key(sk)
        
        if addr != YOUR_ADDRESS:
            print(f"❌ Mnemonic doesn't match address!")
            print(f"Expected: {YOUR_ADDRESS}")
            print(f"Got: {addr}")
            return
            
        print("✅ Address verified")
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
    
    # Simple deployment with defaults
    goal = 2_000_000  # 2 ALGO goal
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 1000  # 1000 rounds (~1 hour)
    receiver = addr  # You are the receiver
    
    print(f"\n📋 Deployment Config:")
    print(f"   Goal: {goal/1_000_000} ALGO")
    print(f"   Deadline: Round {deadline_round} (in 1000 rounds)")
    print(f"   Receiver: {receiver}")
    
    try:
        # Create signer
        signer = algosdk.atomic_transaction_composer.AccountTransactionSigner(sk)
        
        # Deploy
        app_client = client.ApplicationClient(
            client=algod_client,
            app=app,
            signer=signer,
        )
        
        print("Deploying...")
        app_id, app_addr, _ = app_client.create(
            goal_amount=goal,
            deadline_round=deadline_round,
            receiver_addr=receiver,
        )
        
        print(f"\n✅ Deployed Successfully!")
        print(f"   APP_ID: {app_id}")
        print(f"   APP_ADDRESS: {app_addr}")
        print(f"   Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
        # Fund the app for inner transactions
        print(f"\nFunding app with 0.5 ALGO for operations...")
        sp = algod_client.suggested_params()
        fund_txn = algosdk.transaction.PaymentTxn(addr, sp, app_addr, 500_000)
        stx = fund_txn.sign(sk)
        txid = algod_client.send_transaction(stx)
        algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ App funded")
        
        print(f"\n🎯 SAVE THESE:")
        print(f"APP_ID: {app_id}")
        print(f"APP_ADDRESS: {app_addr}")
        
        print(f"\n📱 Next Steps:")
        print(f"1. Open Pera Wallet → TestNet")
        print(f"2. Send 2+ ALGO to: {app_addr}")
        print(f"3. Check: python check_balance_testnet.py")
        print(f"4. Release: python call_release_testnet.py")
        
        return app_id, app_addr
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return None, None

if __name__ == "__main__":
    deploy_to_testnet()