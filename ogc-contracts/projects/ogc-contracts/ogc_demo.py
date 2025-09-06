#!/usr/bin/env python3
"""OGC Demo for CI"""

from beaker import sandbox, client
from working_vault import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner

def ogc_demo():
    print("🚀 OGC - Out The Groupchat Demo")
    
    algod_client = sandbox.get_algod_client()
    organizer = sandbox.get_accounts().pop()
    alice = sandbox.get_accounts().pop()
    
    goal = 2_000_000  # 2 ALGO
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 50
    
    print(f"🎯 Goal: {goal/1_000_000} ALGO")
    
    # Deploy
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=organizer.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=goal,
        deadline_round=deadline_round,
        receiver_addr=organizer.address,
    )
    
    print(f"✅ Fund Created: APP_ID {app_id}")
    
    # Fund app
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(organizer.address, sp, app_addr, 3_000_000)
    algod_client.send_transaction(fund_txn.sign(organizer.private_key))
    
    # Alice contributes
    alice_amount = 1_500_000
    pmt = tx.PaymentTxn(alice.address, sp, app_addr, alice_amount)
    pmt_signed = TransactionWithSigner(pmt, alice.signer)
    
    app_client_alice = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=alice.signer
    )
    app_client_alice.call("contribute", payment=pmt_signed)
    
    total = app_client.call("get_total").return_value
    print(f"💰 Total: {total/1_000_000} ALGO")
    
    if total >= goal:
        print("🎉 Goal reached!")
    else:
        print(f"⏳ Need {(goal-total)/1_000_000} more ALGO")
    
    return {"app_id": app_id, "total": total, "goal": goal}

if __name__ == "__main__":
    result = ogc_demo()
    print(f"🏁 Demo complete: {result['total']/1_000_000} ALGO raised")