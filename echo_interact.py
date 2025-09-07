#!/usr/bin/env python3
"""
Interact with Echo Contract - Test automatic ALGO bounce-back
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def load_echo_deployment():
    """Load echo deployment info"""
    if not os.path.exists("echo_contract_deployment.json"):
        print("❌ No echo_contract_deployment.json found")
        print("Deploy echo contract first: python echo_contract.py")
        return None
    
    with open("echo_contract_deployment.json", 'r') as f:
        return json.load(f)

def test_echo():
    """Test echo functionality - send ALGO and get it back"""
    echo_info = load_echo_deployment()
    if not echo_info:
        return
    
    print("🔄 Test Echo Contract")
    print(f"   APP_ID: {echo_info['appId']}")
    print(f"   Address: {echo_info['appAddress']}")
    
    # Select wallet
    tester = select_wallet()
    if not tester:
        return
    
    # Get test amount
    amount_algo = float(input("Amount to echo test (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    print(f"\n🧪 Echo Test:")
    print(f"   Sending: {amount_algo} ALGO")
    print(f"   Expected back: ~{amount_algo - 0.001} ALGO")
    print(f"   Fee: 0.001 ALGO")
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Check balance before
    try:
        before_info = algod_client.account_info(tester['addr'])
        balance_before = before_info['amount'] / 1_000_000
        print(f"   Balance before: {balance_before} ALGO")
    except Exception as e:
        print(f"❌ Could not check balance: {e}")
        return
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create payment transaction
    pay_txn = transaction.PaymentTxn(
        sender=tester['addr'],
        sp=sp,
        receiver=echo_info['appAddress'],
        amt=amount_micro
    )
    
    # Create app call transaction
    app_call_txn = transaction.ApplicationNoOpTxn(
        sender=tester['addr'],
        sp=sp,
        index=echo_info['appId'],
        app_args=[b"echo"]
    )
    
    # Group transactions
    transaction.assign_group_id([pay_txn, app_call_txn])
    
    # Sign transactions
    signed_pay = pay_txn.sign(tester['sk'])
    signed_call = app_call_txn.sign(tester['sk'])
    
    try:
        # Send grouped transaction
        tx_id = algod_client.send_transactions([signed_pay, signed_call])
        print(f"\n📤 Sent echo test tx: {tx_id}")
        
        # Wait for confirmation
        print("⏳ Waiting for echo...")
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        
        # Check balance after
        after_info = algod_client.account_info(tester['addr'])
        balance_after = after_info['amount'] / 1_000_000
        
        net_change = balance_after - balance_before
        
        print(f"\n✅ Echo Complete!")
        print(f"   Balance after: {balance_after} ALGO")
        print(f"   Net change: {net_change:.6f} ALGO")
        print(f"   TX: https://testnet.algoexplorer.io/tx/{tx_id}")
        
        if net_change > -0.01:  # Allow for small fees
            print(f"   🎉 SUCCESS! ALGO bounced back!")
        else:
            print(f"   ⚠️  Unexpected loss: {abs(net_change)} ALGO")
        
    except Exception as e:
        print(f"❌ Echo test failed: {e}")

def check_echo_stats():
    """Check echo contract statistics"""
    echo_info = load_echo_deployment()
    if not echo_info:
        return
    
    print("📊 Echo Contract Stats")
    print(f"   APP_ID: {echo_info['appId']}")
    print(f"   Address: {echo_info['appAddress']}")
    
    # Check contract balance
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    try:
        account_info = algod_client.account_info(echo_info['appAddress'])
        balance = account_info['amount'] / 1_000_000
        
        print(f"   Contract Balance: {balance} ALGO")
        print(f"   Status: {'✅ Ready' if balance > 0.1 else '⚠️ Low balance'}")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{echo_info['appAddress']}")
        
        if balance < 0.1:
            print(f"\n💡 Tip: Fund contract with more ALGO for testing")
        
    except Exception as e:
        print(f"   ❌ Could not check stats: {e}")

def fund_echo_contract():
    """Fund echo contract for operations"""
    echo_info = load_echo_deployment()
    if not echo_info:
        return
    
    print("💰 Fund Echo Contract")
    
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
        receiver=echo_info['appAddress'],
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
        print(f"✅ Funded echo contract with {amount_algo} ALGO")
        
    except Exception as e:
        print(f"❌ Funding failed: {e}")

def main():
    """Main echo interaction menu"""
    while True:
        print("\n🔄 Echo Contract Interaction")
        print("1. Test echo (send ALGO, get it back)")
        print("2. Check contract stats")
        print("3. Fund contract")
        print("4. Exit")
        
        choice = input("Choose (1-4): ").strip()
        
        if choice == "1":
            test_echo()
        elif choice == "2":
            check_echo_stats()
        elif choice == "3":
            fund_echo_contract()
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()