#!/usr/bin/env python3
"""
Interact with Advanced Vault Contract
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction
from wallet_selector import select_wallet, load_wallets

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def load_vault_deployment():
    """Load vault deployment info"""
    if not os.path.exists("advanced_vault_deployment.json"):
        print("❌ No advanced_vault_deployment.json found")
        print("Deploy vault first: python advanced_vault.py")
        return None
    
    with open("advanced_vault_deployment.json", 'r') as f:
        return json.load(f)

def contribute_to_vault():
    """Contribute ALGO to vault"""
    vault_info = load_vault_deployment()
    if not vault_info:
        return
    
    print("💰 Contribute to Advanced Vault")
    print(f"   APP_ID: {vault_info['appId']}")
    print(f"   Goal: {vault_info['goal']/1_000_000} ALGO")
    
    # Select wallet
    contributor = select_wallet()
    if not contributor:
        return
    
    # Get contribution amount
    amount_algo = float(input("Contribution amount (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create payment transaction
    pay_txn = transaction.PaymentTxn(
        sender=contributor['addr'],
        sp=sp,
        receiver=vault_info['appAddress'],
        amt=amount_micro
    )
    
    # Create app call transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=contributor['addr'],
        sp=sp,
        index=vault_info['appId'],
        app_args=[b"contribute"]
    )
    
    # Group transactions
    transaction.assign_group_id([pay_txn, app_call_txn])
    
    # Sign transactions
    signed_pay = pay_txn.sign(contributor['sk'])
    signed_call = app_call_txn.sign(contributor['sk'])
    
    # Send grouped transaction
    tx_id = algod_client.send_transactions([signed_pay, signed_call])
    print(f"Sent contribution tx: {tx_id}")
    
    # Wait for confirmation
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print(f"✅ Contributed {amount_algo} ALGO to vault!")

def release_vault_funds():
    """Release vault funds to receiver"""
    vault_info = load_vault_deployment()
    if not vault_info:
        return
    
    print("🚀 Release Vault Funds")
    
    # Select wallet (anyone can call release)
    caller = select_wallet()
    if not caller:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create app call transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=caller['addr'],
        sp=sp,
        index=vault_info['appId'],
        app_args=[b"release"]
    )
    
    # Sign transaction
    signed_call = app_call_txn.sign(caller['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_call)
        print(f"Sent release tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Vault funds released to receiver!")
        
    except Exception as e:
        print(f"❌ Release failed: {e}")
        if "deadline" in str(e).lower():
            print("   Deadline may not have passed yet")
        if "goal" in str(e).lower():
            print("   Goal may not have been reached")

def check_vault_status():
    """Check vault status"""
    vault_info = load_vault_deployment()
    if not vault_info:
        return
    
    print("📊 Vault Status")
    print(f"   APP_ID: {vault_info['appId']}")
    print(f"   Address: {vault_info['appAddress']}")
    print(f"   Goal: {vault_info['goal']/1_000_000} ALGO")
    print(f"   Receiver: {vault_info['receiver']}")
    
    # Check balance
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    try:
        account_info = algod_client.account_info(vault_info['appAddress'])
        balance = account_info['amount'] / 1_000_000
        print(f"   Current Balance: {balance} ALGO")
        
        goal_reached = balance >= (vault_info['goal'] / 1_000_000)
        print(f"   Goal Reached: {'✅' if goal_reached else '❌'}")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{vault_info['appAddress']}")
        
    except Exception as e:
        print(f"   ❌ Could not check balance: {e}")

def main():
    """Main interaction menu"""
    while True:
        print("\n🏦 Advanced Vault Interaction")
        print("1. Contribute to vault")
        print("2. Release vault funds")
        print("3. Check vault status")
        print("4. Exit")
        
        choice = input("Choose (1-4): ").strip()
        
        if choice == "1":
            contribute_to_vault()
        elif choice == "2":
            release_vault_funds()
        elif choice == "3":
            check_vault_status()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()