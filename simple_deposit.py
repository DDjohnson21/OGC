#!/usr/bin/env python3
"""
Interacts with the app:
  python simple_deposit.py optin
  python simple_deposit.py deposit 1
  python simple_deposit.py info

Deposits must be grouped as [AppCall("deposit"), Payment], both from the same sender.
When your cumulative deposits reach 2 ALGO, the app inner-sends 2 ALGO back and logs "success".
"""

import json
import os
import sys
import base64
from algosdk.v2client import algod
from algosdk import mnemonic, account, transaction, logic
from algosdk.transaction import (
    ApplicationOptInTxn, ApplicationCallTxn, PaymentTxn, OnComplete, assign_group_id
)

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # not needed for Algonode

# File paths
WALLET_PATH = os.path.join(os.path.dirname(__file__), "permanent_wallet.json")
DEPLOY_PATH = os.path.join(os.path.dirname(__file__), "simple_deployment.json")


def load_account():
    """Load account from permanent_wallet.json"""
    with open(WALLET_PATH, 'r') as f:
        wallet_data = json.load(f)
    
    # Get private key from mnemonic
    private_key = mnemonic.to_private_key(wallet_data['mnemonic'])
    derived_addr = account.address_from_private_key(private_key)
    
    if derived_addr != wallet_data['addr']:
        raise ValueError("Wallet address does not match mnemonic in permanent_wallet.json")
    
    return {"addr": derived_addr, "sk": private_key}


def load_deployment():
    """Load deployment info from simple_deployment.json"""
    with open(DEPLOY_PATH, 'r') as f:
        deploy_data = json.load(f)
    
    if 'appId' not in deploy_data:
        raise ValueError("simple_deployment.json missing appId")
    
    return deploy_data


def text_arg(s):
    """Convert string to bytes for app arguments"""
    return s.encode('utf-8')


def print_logs_from_tx(algod_client, tx_id):
    """Print logs and inner transactions from a transaction"""
    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    
    # Print logs
    logs = confirmed_txn.get('logs', [])
    if logs:
        decoded_logs = [base64.b64decode(log).decode('utf-8') for log in logs]
        print("App Logs:", decoded_logs)
    
    # Print inner transactions (e.g., 2 ALGO refund)
    inner_txns = confirmed_txn.get('inner-txns', [])
    for i, itx in enumerate(inner_txns):
        if 'txn' in itx and itx['txn'].get('type') == 'pay':
            amount = itx['txn']['amt']
            receiver = itx['txn']['rcv']
            print(f"Inner payment #{i}: {amount} µALGO -> {receiver}")
    
    return confirmed_txn


def do_opt_in(algod_client, acct, app_id):
    """Opt into the application"""
    sp = algod_client.suggested_params()
    
    opt_in_txn = ApplicationOptInTxn(
        sender=acct['addr'],
        sp=sp,
        index=app_id
    )
    
    signed_txn = opt_in_txn.sign(acct['sk'])
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"Sent opt-in tx: {tx_id}")
    transaction.wait_for_confirmation(algod_client, tx_id, 4)
    print("Opt-in confirmed")


def do_info(algod_client, acct, app_id):
    """Call the info function"""
    sp = algod_client.suggested_params()
    
    call_txn = ApplicationCallTxn(
        sender=acct['addr'],
        sp=sp,
        index=app_id,
        on_complete=OnComplete.NoOpOC,
        app_args=[text_arg("info")]
    )
    
    signed_txn = call_txn.sign(acct['sk'])
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"Sent info call tx: {tx_id}")
    print_logs_from_tx(algod_client, tx_id)


def do_deposit(algod_client, acct, app_id, algos):
    """Make a deposit to the application"""
    if not isinstance(algos, (int, float)) or algos <= 0:
        raise ValueError("Deposit amount must be a positive number of ALGOs")
    
    amount = round(algos * 1_000_000)  # Convert to microALGO
    
    sp = algod_client.suggested_params()
    app_addr = logic.get_application_address(app_id)
    
    # 1) App call first
    app_call_txn = ApplicationCallTxn(
        sender=acct['addr'],
        sp=sp,
        index=app_id,
        on_complete=OnComplete.NoOpOC,
        app_args=[text_arg("deposit")]
    )
    
    # 2) Payment second
    pay_txn = PaymentTxn(
        sender=acct['addr'],
        sp=sp,
        receiver=app_addr,
        amt=amount
    )
    
    # Group transactions
    assign_group_id([app_call_txn, pay_txn])
    
    # Sign transactions
    signed_app_call = app_call_txn.sign(acct['sk'])
    signed_payment = pay_txn.sign(acct['sk'])
    
    # Send grouped transaction
    tx_id = algod_client.send_transactions([signed_app_call, signed_payment])
    print(f"Sent grouped deposit txs. Group ID (first tx): {tx_id}")
    
    print_logs_from_tx(algod_client, tx_id)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python simple_deposit.py optin")
        print("  python simple_deposit.py deposit 1")
        print("  python simple_deposit.py info")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd not in ["optin", "deposit", "info"]:
        print("Invalid command. Use: optin, deposit, or info")
        sys.exit(1)
    
    try:
        # Initialize client and load data
        algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
        acct = load_account()
        deployment = load_deployment()
        app_id = deployment['appId']
        
        # Execute command
        if cmd == "optin":
            do_opt_in(algod_client, acct, app_id)
        elif cmd == "info":
            do_info(algod_client, acct, app_id)
        elif cmd == "deposit":
            if len(sys.argv) < 3:
                raise ValueError("Please provide an amount in ALGO, e.g. 'deposit 1'")
            amount = float(sys.argv[2])
            do_deposit(algod_client, acct, app_id, amount)
    
    except Exception as e:
        error_msg = str(e).lower()
        if "already opted in" in error_msg:
            print("Already opted-in. You can proceed to deposit.")
            return
        
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
