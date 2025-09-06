#!/usr/bin/env python3
"""Fund the deployed app for inner transactions"""

from beaker import sandbox
from algosdk import transaction as tx

def main():
    algod = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    sp = algod.suggested_params()
    
    app_addr = input("Paste APP_ADDRESS: ").strip()
    
    # Fund with 3 ALGO for inner transactions
    txn = tx.PaymentTxn(acct.address, sp, app_addr, 3_000_000)
    signed_txn = txn.sign(acct.private_key)
    
    txid = algod.send_transaction(signed_txn)
    print(f"Funding transaction sent: {txid}")
    print("App funded with 3 ALGO for inner transactions")

if __name__ == "__main__":
    main()