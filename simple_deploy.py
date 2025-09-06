#!/usr/bin/env python3
"""
Deploys the TEAL app and writes simple_deployment.json with the appId
Network: TestNet via Algonode (no token needed)
"""

import json
import os
import base64
from algosdk.v2client import algod
from algosdk import mnemonic, account, transaction, logic
from algosdk.transaction import ApplicationCreateTxn, OnComplete

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # not needed for Algonode

# File paths
APPROVAL_PATH = os.path.join(os.path.dirname(__file__), "simple_approval.teal")
CLEAR_PATH = os.path.join(os.path.dirname(__file__), "simple_clear.teal")
WALLET_PATH = os.path.join(os.path.dirname(__file__), "permanent_wallet.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "simple_deployment.json")


def load_account():
    """Load account from permanent_wallet.json"""
    with open(WALLET_PATH, 'r') as f:
        wallet_data = json.load(f)
    
    if not wallet_data or 'mnemonic' not in wallet_data:
        raise ValueError("permanent_wallet.json missing 'mnemonic'")
    if 'addr' not in wallet_data:
        raise ValueError("permanent_wallet.json missing 'addr'")
    
    # Get private key from mnemonic
    private_key = mnemonic.to_private_key(wallet_data['mnemonic'])
    derived_addr = account.address_from_private_key(private_key)
    file_addr = wallet_data['addr'].strip()
    
    # Validate address
    if not account.is_valid(file_addr):
        raise ValueError(f"'addr' in permanent_wallet.json is not a valid Algorand address: {file_addr}")
    
    # Warn if addresses don't match
    if derived_addr != file_addr:
        print(f"Warning: mnemonic-derived address != file address.")
        print(f"  derived: {derived_addr}")
        print(f"  file:    {file_addr}")
        print("Proceeding with the file address.")
    
    return {"addr": file_addr, "sk": private_key}


def compile_teal(algod_client, teal_source):
    """Compile TEAL source code"""
    compile_response = algod_client.compile(teal_source)
    return base64.b64decode(compile_response['result'])


def main():
    """Main deployment function"""
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Load account
    creator = load_account()
    
    # Read TEAL files
    with open(APPROVAL_PATH, 'r') as f:
        approval_teal = f.read()
    
    with open(CLEAR_PATH, 'r') as f:
        clear_teal = f.read()
    
    print("Compiling TEAL...")
    approval_prog = compile_teal(algod_client, approval_teal)
    clear_prog = compile_teal(algod_client, clear_teal)
    
    # Schema: 1 local uint ("d"); no globals
    local_ints = 1
    local_bytes = 0
    global_ints = 0
    global_bytes = 0
    
    print(f"Using sender address: {creator['addr']}")
    
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
    
    print(f"Deployed App ID: {app_id}")
    print(f"App Address: {app_addr}")
    
    # Write deployment info
    deployment_info = {
        "appId": app_id,
        "appAddress": app_addr,
        "network": "testnet"
    }
    
    with open(OUT_PATH, 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
