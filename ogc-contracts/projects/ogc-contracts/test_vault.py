#!/usr/bin/env python3
"""Test suite for OGC Vault"""

from beaker import sandbox, client
from working_vault import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner

def test_vault_basic():
    print("🧪 Testing OGC Vault Basic Flow")
    
    algod_client = sandbox.get_algod_client()
    creator = sandbox.get_accounts().pop()
    contributor = sandbox.get_accounts().pop()
    
    goal = 1_000_000  # 1 ALGO
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 100
    
    # Deploy
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=creator.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=goal,
        deadline_round=deadline_round,
        receiver_addr=creator.address,
    )
    
    print(f"✅ Deployed: APP_ID {app_id}")
    
    # Fund app
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(creator.address, sp, app_addr, 2_000_000)
    algod_client.send_transaction(fund_txn.sign(creator.private_key))
    
    # Test contribution
    contrib_amount = 500_000
    pmt = tx.PaymentTxn(contributor.address, sp, app_addr, contrib_amount)
    pmt_with_signer = TransactionWithSigner(pmt, contributor.signer)
    
    app_client_contrib = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=contributor.signer
    )
    app_client_contrib.call("contribute", payment=pmt_with_signer)
    
    # Verify
    total = app_client.call("get_total").return_value
    goal_check = app_client.call("get_goal").return_value
    
    assert total == contrib_amount, f"Expected {contrib_amount}, got {total}"
    assert goal_check == goal, f"Expected {goal}, got {goal_check}"
    
    print(f"✅ Contribution test passed: {total/1_000_000} ALGO")
    return True

if __name__ == "__main__":
    success = test_vault_basic()
    print(f"🏁 Tests {'PASSED' if success else 'FAILED'}")