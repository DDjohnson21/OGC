#!/usr/bin/env python3
"""
Echo Contract - Automatically bounces ALGO back to sender
Perfect for testing and demos
"""

import json
import os
import base64
from algosdk.v2client import algod
from algosdk import transaction, logic
from algosdk.transaction import ApplicationCreateTxn, OnComplete
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def get_echo_contract_teal():
    """Generate echo contract TEAL code"""
    approval_teal = """#pragma version 8

// Echo Contract - Bounces ALGO back to sender
// Global state: total_echoed, echo_count

txn ApplicationID
int 0
==
bnz create_app

// Handle application calls
txn OnCompletion
int NoOp
==
bnz handle_noop

// Reject other operations
int 0
return

create_app:
    // Initialize counters
    byte "total_echoed"
    int 0
    app_global_put
    
    byte "echo_count"
    int 0
    app_global_put
    
    int 1
    return

handle_noop:
    // Check method call
    txn ApplicationArgs 0
    byte "echo"
    ==
    bnz echo_payment
    
    txn ApplicationArgs 0
    byte "get_stats"
    ==
    bnz get_stats
    
    int 0
    return

echo_payment:
    // Verify payment transaction in group
    gtxn 0 TypeEnum
    int pay
    ==
    assert
    
    gtxn 0 Receiver
    global CurrentApplicationAddress
    ==
    assert
    
    gtxn 0 Amount
    int 0
    >
    assert
    
    // Calculate echo amount (original - fee)
    gtxn 0 Amount
    int 1000  // 0.001 ALGO fee
    -
    store 0   // Store echo amount
    
    // Send ALGO back to sender
    itxn_begin
    int pay
    itxn_field TypeEnum
    gtxn 0 Sender
    itxn_field Receiver
    load 0
    itxn_field Amount
    itxn_submit
    
    // Update statistics
    byte "total_echoed"
    byte "total_echoed"
    app_global_get
    gtxn 0 Amount
    +
    app_global_put
    
    byte "echo_count"
    byte "echo_count"
    app_global_get
    int 1
    +
    app_global_put
    
    int 1
    return

get_stats:
    // Return stats (for info)
    int 1
    return
"""

    clear_teal = """#pragma version 8
int 1
return
"""
    
    return approval_teal, clear_teal

def compile_teal(algod_client, teal_source):
    """Compile TEAL source code"""
    compile_response = algod_client.compile(teal_source)
    return base64.b64decode(compile_response['result'])

def deploy_echo_contract():
    """Deploy echo contract"""
    print("🔄 Deploy Echo Contract")
    print("Automatically bounces ALGO back to sender (minus 0.001 ALGO fee)")
    
    # Select wallet
    creator = select_wallet()
    if not creator:
        print("❌ No wallet selected")
        return
    
    print(f"Deploying echo contract with: {creator['addr']}")
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get TEAL code
    approval_teal, clear_teal = get_echo_contract_teal()
    
    print("Compiling TEAL...")
    approval_prog = compile_teal(algod_client, approval_teal)
    clear_prog = compile_teal(algod_client, clear_teal)
    
    # Schema: 2 global values
    local_ints = 0
    local_bytes = 0
    global_ints = 2  # total_echoed, echo_count
    global_bytes = 0
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create application creation transaction
    txn = ApplicationCreateTxn(
        sender=creator['addr'],
        sp=sp,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_prog,
        clear_program=clear_prog,
        global_schema=transaction.StateSchema(global_ints, global_bytes),
        local_schema=transaction.StateSchema(local_ints, local_bytes)
    )
    
    # Sign transaction
    signed_txn = txn.sign(creator['sk'])
    
    # Send transaction
    tx_id = algod_client.send_transaction(signed_txn)
    print(f"Sent app create tx: {tx_id}")
    
    # Wait for confirmation
    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    app_id = confirmed_txn["application-index"]
    
    if not app_id:
        raise ValueError("No application-index in create confirmation!")
    
    # Get app address
    app_addr = logic.get_application_address(app_id)
    
    print(f"✅ Echo Contract Deployed!")
    print(f"   APP_ID: {app_id}")
    print(f"   App Address: {app_addr}")
    print(f"   Deployed by: {creator['name']}")
    
    # Fund the contract for operations
    fund = input("Fund contract with ALGO for echo operations? (y/N): ").strip().lower()
    if fund == 'y':
        amount = float(input("Amount to fund (ALGO): "))
        fund_amount = int(amount * 1_000_000)
        
        # Send funding transaction
        fund_txn = transaction.PaymentTxn(
            sender=creator['addr'],
            sp=sp,
            receiver=app_addr,
            amt=fund_amount
        )
        
        signed_fund = fund_txn.sign(creator['sk'])
        fund_tx_id = algod_client.send_transaction(signed_fund)
        transaction.wait_for_confirmation(algod_client, fund_tx_id, 4)
        print(f"✅ Funded contract with {amount} ALGO")
    
    # Save deployment info
    deployment_info = {
        "appId": app_id,
        "appAddress": app_addr,
        "network": "testnet",
        "deployedBy": creator['name'],
        "type": "echo_contract",
        "description": "Bounces ALGO back to sender"
    }
    
    with open("echo_contract_deployment.json", 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Wrote echo_contract_deployment.json")
    print(f"\n🎯 How to Test:")
    print(f"1. Send ALGO to: {app_addr}")
    print(f"2. Use: python echo_interact.py")
    print(f"3. Watch ALGO bounce back!")

if __name__ == "__main__":
    try:
        deploy_echo_contract()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)