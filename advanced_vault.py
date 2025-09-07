#!/usr/bin/env python3
"""
Advanced Vault Contract - Goal-based crowdfunding with deadline
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

def get_advanced_vault_teal():
    """Generate advanced vault TEAL code"""
    approval_teal = """#pragma version 8

// Advanced Vault Contract
// Global state: goal (uint64), deadline (uint64), receiver (bytes), total (uint64)

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
    // Initialize global state
    // goal = Txn.ApplicationArgs[0]
    byte "goal"
    txn ApplicationArgs 0
    btoi
    app_global_put
    
    // deadline = Txn.ApplicationArgs[1] 
    byte "deadline"
    txn ApplicationArgs 1
    btoi
    app_global_put
    
    // receiver = Txn.ApplicationArgs[2]
    byte "receiver"
    txn ApplicationArgs 2
    app_global_put
    
    // total = 0
    byte "total"
    int 0
    app_global_put
    
    int 1
    return

handle_noop:
    // Check method call
    txn ApplicationArgs 0
    byte "contribute"
    ==
    bnz contribute
    
    txn ApplicationArgs 0
    byte "release"
    ==
    bnz release
    
    txn ApplicationArgs 0
    byte "get_info"
    ==
    bnz get_info
    
    int 0
    return

contribute:
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
    
    // Update total
    byte "total"
    byte "total"
    app_global_get
    gtxn 0 Amount
    +
    app_global_put
    
    int 1
    return

release:
    // Check if goal reached and deadline passed
    global LatestTimestamp
    byte "deadline"
    app_global_get
    >=
    assert
    
    global CurrentApplicationAddress
    balance
    byte "goal"
    app_global_get
    >=
    assert
    
    // Send funds to receiver
    itxn_begin
    int pay
    itxn_field TypeEnum
    byte "receiver"
    app_global_get
    itxn_field Receiver
    global CurrentApplicationAddress
    balance
    int 100000  // Keep min balance
    -
    itxn_field Amount
    itxn_submit
    
    int 1
    return

get_info:
    // Return contract info (for debugging)
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

def deploy_advanced_vault():
    """Deploy advanced vault with parameters"""
    print("🏦 Deploy Advanced Vault Contract")
    
    # Select wallet
    creator = select_wallet()
    if not creator:
        print("❌ No wallet selected")
        return
    
    # Get parameters
    goal_algo = float(input("Goal amount (ALGO): "))
    goal_micro = int(goal_algo * 1_000_000)
    
    deadline_hours = int(input("Deadline (hours from now): "))
    deadline_timestamp = int(transaction.wait_for_confirmation.__globals__['time'].time()) + (deadline_hours * 3600)
    
    receiver = input(f"Receiver address (or press Enter for deployer): ").strip()
    if not receiver:
        receiver = creator['addr']
    
    print(f"\n📋 Vault Config:")
    print(f"   Goal: {goal_algo} ALGO")
    print(f"   Deadline: {deadline_hours} hours from now")
    print(f"   Receiver: {receiver}")
    
    confirm = input("Deploy? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get TEAL code
    approval_teal, clear_teal = get_advanced_vault_teal()
    
    print("Compiling TEAL...")
    approval_prog = compile_teal(algod_client, approval_teal)
    clear_prog = compile_teal(algod_client, clear_teal)
    
    # Schema: 4 global values
    local_ints = 0
    local_bytes = 0
    global_ints = 3  # goal, deadline, total
    global_bytes = 1  # receiver
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Application arguments
    app_args = [
        goal_micro.to_bytes(8, 'big'),
        deadline_timestamp.to_bytes(8, 'big'),
        receiver.encode()
    ]
    
    # Create application creation transaction
    txn = ApplicationCreateTxn(
        sender=creator['addr'],
        sp=sp,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_prog,
        clear_program=clear_prog,
        global_schema=transaction.StateSchema(global_ints, global_bytes),
        local_schema=transaction.StateSchema(local_ints, local_bytes),
        app_args=app_args
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
    
    print(f"✅ Advanced Vault Deployed!")
    print(f"   APP_ID: {app_id}")
    print(f"   App Address: {app_addr}")
    print(f"   Goal: {goal_algo} ALGO")
    print(f"   Deployed by: {creator['name']}")
    
    # Save deployment info
    deployment_info = {
        "appId": app_id,
        "appAddress": app_addr,
        "goal": goal_micro,
        "deadline": deadline_timestamp,
        "receiver": receiver,
        "network": "testnet",
        "deployedBy": creator['name'],
        "type": "advanced_vault"
    }
    
    with open("advanced_vault_deployment.json", 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Wrote advanced_vault_deployment.json")
    print(f"\n🎯 Next Steps:")
    print(f"1. Send ALGO to: {app_addr}")
    print(f"2. Use: python vault_interact.py")

if __name__ == "__main__":
    try:
        import time
        transaction.wait_for_confirmation.__globals__['time'] = __import__('time')
        deploy_advanced_vault()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)