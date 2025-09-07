#!/usr/bin/env python3
"""
Governance Sender Contract - Requires 75% contributor approval before sending
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

def get_governance_sender_teal():
    """Generate governance sender contract TEAL code"""
    approval_teal = """#pragma version 8

// Governance Sender Contract
// Global state: owner, total_contributors, total_sent
// Local state: contributed_amount, voted_for_proposal

txn ApplicationID
int 0
==
bnz create_app

// Handle application calls
txn OnCompletion
int OptIn
==
bnz opt_in

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
    
    // Initialize counters
    byte "total_contributors"
    int 0
    app_global_put
    
    byte "total_sent"
    int 0
    app_global_put
    
    byte "active_proposal"
    int 0
    app_global_put
    
    int 1
    return

opt_in:
    // Initialize local state for new contributor
    byte "contributed"
    int 0
    app_local_put
    
    byte "voted"
    int 0
    app_local_put
    
    int 1
    return

handle_noop:
    // Check method call
    txn ApplicationArgs 0
    byte "contribute"
    ==
    bnz contribute
    
    txn ApplicationArgs 0
    byte "propose_send"
    ==
    bnz propose_send
    
    txn ApplicationArgs 0
    byte "vote"
    ==
    bnz vote
    
    txn ApplicationArgs 0
    byte "execute_send"
    ==
    bnz execute_send
    
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
    
    // Check if first contribution from this user
    byte "contributed"
    app_local_get
    int 0
    ==
    bnz first_contribution
    
    // Update existing contribution
    byte "contributed"
    byte "contributed"
    app_local_get
    gtxn 0 Amount
    +
    app_local_put
    
    b contribution_done

first_contribution:
    // First contribution - increment contributor count
    byte "total_contributors"
    byte "total_contributors"
    app_global_get
    int 1
    +
    app_global_put
    
    // Set contribution amount
    byte "contributed"
    gtxn 0 Amount
    app_local_put

contribution_done:
    int 1
    return

propose_send:
    // Only owner can propose
    txn Sender
    byte "owner"
    app_global_get
    ==
    assert
    
    // Check no active proposal
    byte "active_proposal"
    app_global_get
    int 0
    ==
    assert
    
    // Store proposal details in global state
    byte "proposal_recipient"
    txn ApplicationArgs 1
    app_global_put
    
    byte "proposal_amount"
    txn ApplicationArgs 2
    btoi
    app_global_put
    
    byte "proposal_votes"
    int 0
    app_global_put
    
    byte "active_proposal"
    int 1
    app_global_put
    
    int 1
    return

vote:
    // Check there's an active proposal
    byte "active_proposal"
    app_global_get
    int 1
    ==
    assert
    
    // Check user is a contributor
    byte "contributed"
    app_local_get
    int 0
    >
    assert
    
    // Check user hasn't voted yet
    byte "voted"
    app_local_get
    int 0
    ==
    assert
    
    // Record vote
    byte "voted"
    int 1
    app_local_put
    
    // Increment vote count
    byte "proposal_votes"
    byte "proposal_votes"
    app_global_get
    int 1
    +
    app_global_put
    
    int 1
    return

execute_send:
    // Check there's an active proposal
    byte "active_proposal"
    app_global_get
    int 1
    ==
    assert
    
    // Check 75% approval
    // votes * 4 >= contributors * 3 (75% = 3/4)
    byte "proposal_votes"
    app_global_get
    int 4
    *
    
    byte "total_contributors"
    app_global_get
    int 3
    *
    
    >=
    assert
    
    // Execute the send
    itxn_begin
    int pay
    itxn_field TypeEnum
    byte "proposal_recipient"
    app_global_get
    itxn_field Receiver
    byte "proposal_amount"
    app_global_get
    itxn_field Amount
    itxn_submit
    
    // Update total sent
    byte "total_sent"
    byte "total_sent"
    app_global_get
    byte "proposal_amount"
    app_global_get
    +
    app_global_put
    
    // Clear proposal
    byte "active_proposal"
    int 0
    app_global_put
    
    byte "proposal_votes"
    int 0
    app_global_put
    
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

def deploy_governance_sender():
    """Deploy governance sender contract"""
    print("🗳️  Deploy Governance Sender Contract")
    print("Requires 75% contributor approval before sending ALGO")
    
    # Select wallet
    creator = select_wallet()
    if not creator:
        print("❌ No wallet selected")
        return
    
    print(f"Deploying governance contract with owner: {creator['addr']}")
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get TEAL code
    approval_teal, clear_teal = get_governance_sender_teal()
    
    print("Compiling TEAL...")
    approval_prog = compile_teal(algod_client, approval_teal)
    clear_prog = compile_teal(algod_client, clear_teal)
    
    # Schema: global and local state
    local_ints = 2  # contributed, voted
    local_bytes = 0
    global_ints = 4  # total_contributors, total_sent, active_proposal, proposal_votes, proposal_amount
    global_bytes = 2  # owner, proposal_recipient
    
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
    
    print(f"✅ Governance Sender Deployed!")
    print(f"   APP_ID: {app_id}")
    print(f"   App Address: {app_addr}")
    print(f"   Owner: {creator['addr']}")
    print(f"   Governance: 75% contributor approval required")
    
    # Save deployment info
    deployment_info = {
        "appId": app_id,
        "appAddress": app_addr,
        "owner": creator['addr'],
        "network": "testnet",
        "deployedBy": creator['name'],
        "type": "governance_sender",
        "governance": "75% contributor approval"
    }
    
    with open("governance_sender_deployment.json", 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Wrote governance_sender_deployment.json")
    print(f"\n🎯 Next Steps:")
    print(f"1. Contributors opt in: python governance_interact.py")
    print(f"2. Contributors contribute ALGO")
    print(f"3. Owner proposes sends")
    print(f"4. Contributors vote (75% needed)")
    print(f"5. Execute approved sends")

if __name__ == "__main__":
    try:
        deploy_governance_sender()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)