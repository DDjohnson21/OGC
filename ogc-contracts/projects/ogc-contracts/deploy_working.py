#!/usr/bin/env python3
"""Deploy working vault"""

from beaker import sandbox, client
from working_vault import app

def main():
    algod_client = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    
    goal = 1_000_000  # 1 ALGO
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 1000
    receiver = acct.address
    
    print(f"Deploying Working Vault...")
    print(f"  Goal: {goal} microALGO")
    print(f"  Deadline: Round {deadline_round}")
    print(f"  Receiver: {receiver}")
    
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=acct.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=goal,
        deadline_round=deadline_round,
        receiver_addr=receiver,
    )
    
    print(f"\n✅ Deployed Working Vault:")
    print(f"  APP_ID: {app_id}")
    print(f"  APP_ADDRESS: {app_addr}")
    
    # Fund the app for inner transactions
    from algosdk import transaction as tx
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(acct.address, sp, app_addr, 3_000_000)
    signed_fund = fund_txn.sign(acct.private_key)
    algod_client.send_transaction(signed_fund)
    print(f"  Funded with 3 ALGO for inner transactions")
    
    # Test contribute
    contribute_amount = 500_000  # 0.5 ALGO
    from algosdk.atomic_transaction_composer import TransactionWithSigner
    pmt = tx.PaymentTxn(acct.address, sp, app_addr, contribute_amount)
    pmt_with_signer = TransactionWithSigner(pmt, acct.signer)
    result = app_client.call("contribute", payment=pmt_with_signer)
    print(f"  Test contribution: {contribute_amount} microALGO - Success!")
    
    # Check total
    total_result = app_client.call("get_total")
    print(f"  Current total: {total_result.return_value} microALGO")

if __name__ == "__main__":
    main()