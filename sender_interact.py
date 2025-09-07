#!/usr/bin/env python3
"""
Interact with Sender Contract
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction, encoding
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def load_sender_deployment():
    """Load sender deployment info"""
    if not os.path.exists("sender_contract_deployment.json"):
        print("❌ No sender_contract_deployment.json found")
        print("Deploy sender first: python sender_contract.py")
        return None
    
    with open("sender_contract_deployment.json", 'r') as f:
        return json.load(f)

def send_from_contract():
    """Send ALGO from contract to any address"""
    sender_info = load_sender_deployment()
    if not sender_info:
        return
    
    print("📤 Send ALGO from Contract")
    print(f"   APP_ID: {sender_info['appId']}")
    print(f"   Owner: {sender_info['owner']}")
    
    # Select wallet (must be owner)
    caller = select_wallet()
    if not caller:
        return
    
    if caller['addr'] != sender_info['owner']:
        print(f"❌ Only owner can send from contract")
        print(f"   Owner: {sender_info['owner']}")
        print(f"   You: {caller['addr']}")
        return
    
    # Get recipient and amount
    recipient = input("Recipient address: ").strip()
    
    # Validate recipient address
    if not encoding.is_valid_address(recipient):
        print("❌ Invalid recipient address")
        return
    
    amount_algo = float(input("Amount to send (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Check contract balance first
    try:
        account_info = algod_client.account_info(sender_info['appAddress'])
        balance = account_info['amount']
        
        if balance < amount_micro + 100000:  # Need extra for fees
            print(f"❌ Insufficient contract balance")
            print(f"   Contract has: {balance/1_000_000} ALGO")
            print(f"   Trying to send: {amount_algo} ALGO")
            return
            
    except Exception as e:
        print(f"❌ Could not check contract balance: {e}")
        return
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create app call transaction
    app_args = [
        b"send_algo",
        encoding.decode_address(recipient),
        amount_micro.to_bytes(8, 'big')
    ]
    
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=caller['addr'],
        sp=sp,
        index=sender_info['appId'],
        app_args=app_args
    )
    
    # Sign transaction
    signed_call = app_call_txn.sign(caller['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_call)
        print(f"Sent transaction: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Sent {amount_algo} ALGO to {recipient}")
        print(f"   TX: https://testnet.algoexplorer.io/tx/{tx_id}")
        
    except Exception as e:
        print(f"❌ Send failed: {e}")

def check_sender_status():
    """Check sender contract status"""
    sender_info = load_sender_deployment()
    if not sender_info:
        return
    
    print("📊 Sender Contract Status")
    print(f"   APP_ID: {sender_info['appId']}")
    print(f"   Address: {sender_info['appAddress']}")
    print(f"   Owner: {sender_info['owner']}")
    
    # Check balance
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    try:
        account_info = algod_client.account_info(sender_info['appAddress'])
        balance = account_info['amount'] / 1_000_000
        print(f"   Balance: {balance} ALGO")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{sender_info['appAddress']}")
        
    except Exception as e:
        print(f"   ❌ Could not check balance: {e}")

def fund_sender_contract():
    """Fund the sender contract"""
    sender_info = load_sender_deployment()
    if not sender_info:
        return
    
    print("💰 Fund Sender Contract")
    
    # Select wallet
    funder = select_wallet()
    if not funder:
        return
    
    amount_algo = float(input("Amount to fund (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create funding transaction
    fund_txn = transaction.PaymentTxn(
        sender=funder['addr'],
        sp=sp,
        receiver=sender_info['appAddress'],
        amt=amount_micro
    )
    
    # Sign transaction
    signed_fund = fund_txn.sign(funder['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_fund)
        print(f"Sent funding tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Funded contract with {amount_algo} ALGO")
        
    except Exception as e:
        print(f"❌ Funding failed: {e}")

def main():
    """Main interaction menu"""
    while True:
        print("\n📤 Sender Contract Interaction")
        print("1. Send ALGO from contract")
        print("2. Fund contract")
        print("3. Check contract status")
        print("4. Exit")
        
        choice = input("Choose (1-4): ").strip()
        
        if choice == "1":
            send_from_contract()
        elif choice == "2":
            fund_sender_contract()
        elif choice == "3":
            check_sender_status()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()