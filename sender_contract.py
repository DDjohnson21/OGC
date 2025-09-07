#!/usr/bin/env python3
"""
Sender Contract - Can send ALGO to any address
Inherits wallet system from existing branch
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

def get_sender_contract_teal():
    """Generate sender contract TEAL code"""
    approval_teal = """#pragma version 8

// Sender Contract - Can send ALGO to any address
// Global state: owner (bytes), total_sent (uint64)

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
    // Set owner to creator
    byte "owner"
    txn Sender
    app_global_put
    
    // Initialize total_sent
    byte "total_sent"
    int 0
    app_global_put
    
    int 1
    return

handle_noop:
    // Check method call
    txn ApplicationArgs 0
    byte "send_algo"
    ==
    bnz send_algo
    
    txn ApplicationArgs 0
    byte "get_balance"
    ==
    bnz get_balance
    
    int 0
    return

send_algo:
    // Only owner can send
    txn Sender
    byte "owner"
    app_global_get
    ==
    assert
    
    // Get recipient from args[1] and amount from args[2]
    txn ApplicationArgs 1
    len
    int 32
    ==
    assert
    
    txn ApplicationArgs 2
    btoi
    int 0
    >
    assert
    
    // Send ALGO to recipient
    itxn_begin
    int pay
    itxn_field TypeEnum
    txn ApplicationArgs 1
    itxn_field Receiver
    txn ApplicationArgs 2
    btoi
    itxn_field Amount
    itxn_submit
    
    // Update total sent
    byte "total_sent"
    byte "total_sent"
    app_global_get
    txn ApplicationArgs 2
    btoi
    +
    app_global_put
    
    int 1
    return

get_balance:
    // Return current balance (for info)
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

def deploy_sender_contract():
    """Deploy sender contract"""
    print("📤 Deploy Sender Contract")
    
    # Select wallet
    creator = select_wallet()
    if not creator:
        print("❌ No wallet selected")
        return
    
    print(f"Deploying sender contract with owner: {creator['addr']}")
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get TEAL code
    approval_teal, clear_teal = get_sender_contract_teal()
    
    print("Compiling TEAL...")
    approval_prog = compile_teal(algod_client, approval_teal)
    clear_prog = compile_teal(algod_client, clear_teal)
    
    # Schema: 2 global values
    local_ints = 0
    local_bytes = 0
    global_ints = 1  # total_sent
    global_bytes = 1  # owner
    
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
    
    print(f"✅ Sender Contract Deployed!")
    print(f"   APP_ID: {app_id}")
    print(f"   App Address: {app_addr}")
    print(f"   Owner: {creator['addr']}")
    print(f"   Deployed by: {creator['name']}")
    
    # Ask if user wants to fund the contract
    fund = input("Fund contract with ALGO? (y/N): ").strip().lower()
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
        "owner": creator['addr'],
        "network": "testnet",
        "deployedBy": creator['name'],
        "type": "sender_contract"
    }
    
    with open("sender_contract_deployment.json", 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Wrote sender_contract_deployment.json")
    print(f"\n🎯 Next Steps:")
    print(f"1. Use: python sender_interact.py")

if __name__ == "__main__":
    try:
        deploy_sender_contract()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)