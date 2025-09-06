#!/usr/bin/env python3
"""Test contribution to the vault"""

from beaker import sandbox, client
import sys
sys.path.append('..')
from smart_contracts.ogc_vault.contract import app
from algosdk import transaction as tx

def main():
    APP_ID = int(input("APP_ID: ").strip())
    AMOUNT = 200_000  # 0.2 ALGO
    
    algod = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    sp = algod.suggested_params()
    
    # Create app client
    app_client = client.ApplicationClient(
        client=algod,
        app=app,
        app_id=APP_ID,
        signer=acct.signer,
    )
    
    # First opt-in to the app
    try:
        app_client.opt_in()
        print("Opted into the app")
    except Exception as e:
        print(f"Opt-in failed (might already be opted in): {e}")
    
    # Create payment transaction
    pmt = tx.PaymentTxn(acct.address, sp, app_client.app_addr, AMOUNT)
    
    # Call contribute method with payment
    result = app_client.call(
        "contribute",
        payment=pmt,
    )
    
    print(f"✅ Contributed {AMOUNT} microALGO ({AMOUNT/1_000_000} ALGO)")
    print(f"Transaction ID: {result.tx_id}")

if __name__ == "__main__":
    main()