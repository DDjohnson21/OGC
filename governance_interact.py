#!/usr/bin/env python3
"""
Interact with Governance Sender Contract
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction, encoding
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def load_governance_deployment():
    """Load governance deployment info"""
    if not os.path.exists("governance_sender_deployment.json"):
        print("❌ No governance_sender_deployment.json found")
        print("Deploy governance contract first: python governance_sender.py")
        return None
    
    with open("governance_sender_deployment.json", 'r') as f:
        return json.load(f)

def opt_in_contributor():
    """Opt into governance contract as contributor"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("🔗 Opt into Governance Contract")
    print(f"   APP_ID: {gov_info['appId']}")
    
    # Select wallet
    contributor = select_wallet()
    if not contributor:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create opt-in transaction
    txn = transaction.ApplicationOptInTxn(
        sender=contributor['addr'],
        sp=sp,
        index=gov_info['appId']
    )
    
    # Sign transaction
    signed_txn = txn.sign(contributor['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Sent opt-in tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ {contributor['name']} opted into governance contract!")
        
    except Exception as e:
        print(f"❌ Opt-in failed: {e}")

def contribute_to_governance():
    """Contribute ALGO to governance contract"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("💰 Contribute to Governance Contract")
    print(f"   APP_ID: {gov_info['appId']}")
    
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
        receiver=gov_info['appAddress'],
        amt=amount_micro
    )
    
    # Create app call transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=contributor['addr'],
        sp=sp,
        index=gov_info['appId'],
        app_args=[b"contribute"]
    )
    
    # Group transactions
    transaction.assign_group_id([pay_txn, app_call_txn])
    
    # Sign transactions
    signed_pay = pay_txn.sign(contributor['sk'])
    signed_call = app_call_txn.sign(contributor['sk'])
    
    try:
        # Send grouped transaction
        tx_id = algod_client.send_transactions([signed_pay, signed_call])
        print(f"Sent contribution tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ {contributor['name']} contributed {amount_algo} ALGO!")
        
    except Exception as e:
        print(f"❌ Contribution failed: {e}")

def propose_send():
    """Propose sending ALGO (owner only)"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("📝 Propose ALGO Send")
    print(f"   APP_ID: {gov_info['appId']}")
    print(f"   Owner: {gov_info['owner']}")
    
    # Select wallet (must be owner)
    proposer = select_wallet()
    if not proposer:
        return
    
    if proposer['addr'] != gov_info['owner']:
        print(f"❌ Only owner can propose sends")
        print(f"   Owner: {gov_info['owner']}")
        print(f"   You: {proposer['addr']}")
        return
    
    # Get proposal details
    recipient = input("Recipient address: ").strip()
    
    # Validate recipient address
    if not encoding.is_valid_address(recipient):
        print("❌ Invalid recipient address")
        return
    
    amount_algo = float(input("Amount to send (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    print(f"\n📋 Proposal:")
    print(f"   To: {recipient}")
    print(f"   Amount: {amount_algo} ALGO")
    print(f"   Requires 75% contributor approval")
    
    confirm = input("Create proposal? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create proposal transaction
    app_args = [
        b"propose_send",
        encoding.decode_address(recipient),
        amount_micro.to_bytes(8, 'big')
    ]
    
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=proposer['addr'],
        sp=sp,
        index=gov_info['appId'],
        app_args=app_args
    )
    
    # Sign transaction
    signed_call = app_call_txn.sign(proposer['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_call)
        print(f"Sent proposal tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Proposal created!")
        print(f"   Contributors can now vote")
        
    except Exception as e:
        print(f"❌ Proposal failed: {e}")

def vote_on_proposal():
    """Vote on active proposal (contributors only)"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("🗳️  Vote on Proposal")
    print(f"   APP_ID: {gov_info['appId']}")
    
    # Select wallet
    voter = select_wallet()
    if not voter:
        return
    
    print(f"Voting as: {voter['name']}")
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create vote transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=voter['addr'],
        sp=sp,
        index=gov_info['appId'],
        app_args=[b"vote"]
    )
    
    # Sign transaction
    signed_call = app_call_txn.sign(voter['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_call)
        print(f"Sent vote tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ {voter['name']} voted YES!")
        
    except Exception as e:
        print(f"❌ Vote failed: {e}")
        if "voted" in str(e).lower():
            print("   You may have already voted")
        if "contributed" in str(e).lower():
            print("   You must contribute first to vote")

def execute_proposal():
    """Execute approved proposal"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("⚡ Execute Approved Proposal")
    print(f"   APP_ID: {gov_info['appId']}")
    
    # Select wallet (anyone can execute)
    executor = select_wallet()
    if not executor:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create execute transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=executor['addr'],
        sp=sp,
        index=gov_info['appId'],
        app_args=[b"execute_send"]
    )
    
    # Sign transaction
    signed_call = app_call_txn.sign(executor['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_call)
        print(f"Sent execute tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Proposal executed!")
        print(f"   ALGO sent to recipient")
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        if "75%" in str(e).lower() or "approval" in str(e).lower():
            print("   Need 75% contributor approval")

def check_governance_status():
    """Check governance contract status"""
    gov_info = load_governance_deployment()
    if not gov_info:
        return
    
    print("📊 Governance Contract Status")
    print(f"   APP_ID: {gov_info['appId']}")
    print(f"   Address: {gov_info['appAddress']}")
    print(f"   Owner: {gov_info['owner']}")
    print(f"   Governance: {gov_info['governance']}")
    
    # Check balance
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    try:
        account_info = algod_client.account_info(gov_info['appAddress'])
        balance = account_info['amount'] / 1_000_000
        print(f"   Balance: {balance} ALGO")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{gov_info['appAddress']}")
        
    except Exception as e:
        print(f"   ❌ Could not check status: {e}")

def main():
    """Main governance interaction menu"""
    while True:
        print("\n🗳️  Governance Sender Interaction")
        print("1. Opt in as contributor")
        print("2. Contribute ALGO")
        print("3. Propose send (owner only)")
        print("4. Vote on proposal")
        print("5. Execute approved proposal")
        print("6. Check contract status")
        print("7. Exit")
        
        choice = input("Choose (1-7): ").strip()
        
        if choice == "1":
            opt_in_contributor()
        elif choice == "2":
            contribute_to_governance()
        elif choice == "3":
            propose_send()
        elif choice == "4":
            vote_on_proposal()
        elif choice == "5":
            execute_proposal()
        elif choice == "6":
            check_governance_status()
        elif choice == "7":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()