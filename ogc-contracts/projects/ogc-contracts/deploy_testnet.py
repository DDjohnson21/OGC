#!/usr/bin/env python3
"""Deploy OGC Vault to TestNet"""

from algosdk.v2client import algod
from algosdk import mnemonic
from beaker import client
from working_vault import app
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def deploy_to_testnet():
    print("🚀 Deploying OGC Vault to TestNet")
    
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
    info = algod_client.account_info(addr)
    balance = info["amount"] / 1_000_000
    print(f"Account balance: {balance} ALGO")
    
    if balance < 0.5:
        print("❌ Need at least 0.5 ALGO for deployment")
        print("Get TestNet ALGO from: https://testnet.algoexplorer.io/dispenser")
        return
    
    # Deployment parameters
    goal = int(input("Goal amount (ALGO): ")) * 1_000_000
    deadline_rounds = int(input("Deadline (rounds from now): "))
    receiver = input("Receiver address (or press Enter for deployer): ").strip()
    
    if not receiver:
        receiver = addr
    
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + deadline_rounds
    
    print(f"\n📋 Deployment Config:")
    print(f"   Goal: {goal/1_000_000} ALGO")
    print(f"   Deadline: Round {deadline_round} (in {deadline_rounds} rounds)")
    print(f"   Receiver: {receiver}")
    
    confirm = input("\nDeploy? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
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
        
        print(f"\n🎯 Next Steps:")
        print(f"1. Send ALGO to: {app_addr}")
        print(f"2. Check balance: python check_balance_testnet.py")
        print(f"3. After deadline: python call_release_testnet.py")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    deploy_to_testnet()