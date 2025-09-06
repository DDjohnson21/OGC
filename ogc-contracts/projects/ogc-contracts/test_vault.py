#!/usr/bin/env python3
"""Comprehensive test suite for OGC Vault"""

from beaker import sandbox, client
from working_vault import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner

def test_vault_complete_flow():
    print("🧪 Testing OGC Vault Complete Flow\n")
    
    # Setup
    algod_client = sandbox.get_algod_client()
    creator = sandbox.get_accounts().pop()
    contributor1 = sandbox.get_accounts().pop()
    contributor2 = sandbox.get_accounts().pop()
    
    goal = 2_000_000  # 2 ALGO goal
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 10  # Short deadline for testing
    receiver = creator.address
    
    print(f"📋 Test Parameters:")
    print(f"   Goal: {goal/1_000_000} ALGO")
    print(f"   Deadline: Round {deadline_round}")
    print(f"   Current Round: {current_round}")
    
    # Deploy
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=creator.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=goal,
        deadline_round=deadline_round,
        receiver_addr=receiver,
    )
    
    print(f"\n✅ Deployed Vault:")
    print(f"   APP_ID: {app_id}")
    print(f"   APP_ADDRESS: {app_addr}")
    
    # Fund app for inner transactions
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(creator.address, sp, app_addr, 3_000_000)
    algod_client.send_transaction(fund_txn.sign(creator.private_key))
    print(f"   Funded with 3 ALGO")
    
    # Test 1: Multiple contributions
    print(f"\n🔄 Test 1: Multiple Contributions")
    
    # Contribution 1: 0.8 ALGO
    contrib1_amount = 800_000
    pmt1 = tx.PaymentTxn(contributor1.address, sp, app_addr, contrib1_amount)
    pmt1_with_signer = TransactionWithSigner(pmt1, contributor1.signer)
    
    app_client_contrib1 = client.ApplicationClient(
        client=algod_client,
        app=app,
        app_id=app_id,
        signer=contributor1.signer,
    )
    app_client_contrib1.call("contribute", payment=pmt1_with_signer)
    
    total1 = app_client.call("get_total").return_value
    print(f"   After contrib1: {total1/1_000_000} ALGO")
    
    # Contribution 2: 0.7 ALGO  
    contrib2_amount = 700_000
    pmt2 = tx.PaymentTxn(contributor2.address, sp, app_addr, contrib2_amount)
    pmt2_with_signer = TransactionWithSigner(pmt2, contributor2.signer)
    
    app_client_contrib2 = client.ApplicationClient(
        client=algod_client,
        app=app,
        app_id=app_id,
        signer=contributor2.signer,
    )
    app_client_contrib2.call("contribute", payment=pmt2_with_signer)
    
    total2 = app_client.call("get_total").return_value
    print(f"   After contrib2: {total2/1_000_000} ALGO")
    
    # Test 2: Check goal status
    print(f"\n📊 Test 2: Goal Status")
    goal_amount = app_client.call("get_goal").return_value
    current_total = app_client.call("get_total").return_value
    
    print(f"   Goal: {goal_amount/1_000_000} ALGO")
    print(f"   Current: {current_total/1_000_000} ALGO")
    print(f"   Progress: {(current_total/goal_amount)*100:.1f}%")
    
    if current_total >= goal_amount:
        print(f"   🎯 GOAL REACHED!")
    else:
        print(f"   ⏳ Need {(goal_amount-current_total)/1_000_000} more ALGO")
    
    # Test 3: Wait for deadline and release
    print(f"\n⏰ Test 3: Release Mechanism")
    current_round = algod_client.status()["last-round"]
    print(f"   Current round: {current_round}")
    print(f"   Deadline round: {deadline_round}")
    
    if current_round >= deadline_round:
        print(f"   ✅ Past deadline - can release")
        if current_total >= goal_amount:
            try:
                receiver_balance_before = algod_client.account_info(receiver)["amount"]
                app_client.call("release")
                receiver_balance_after = algod_client.account_info(receiver)["amount"]
                received = receiver_balance_after - receiver_balance_before
                print(f"   💰 Released {received/1_000_000} ALGO to receiver")
            except Exception as e:
                print(f"   ❌ Release failed: {e}")
        else:
            print(f"   ❌ Goal not reached - cannot release")
    else:
        print(f"   ⏳ Before deadline - cannot release yet")
    
    # Test 4: App balance verification
    print(f"\n💰 Test 4: Balance Verification")
    app_balance = algod_client.account_info(app_addr)["amount"]
    print(f"   App balance: {app_balance/1_000_000} ALGO")
    print(f"   Tracked total: {current_total/1_000_000} ALGO")
    
    return {
        "app_id": app_id,
        "app_address": app_addr,
        "goal": goal_amount,
        "total": current_total,
        "goal_reached": current_total >= goal_amount
    }

if __name__ == "__main__":
    result = test_vault_complete_flow()
    print(f"\n🏁 Test Summary:")
    print(f"   App ID: {result['app_id']}")
    print(f"   Goal Reached: {'✅' if result['goal_reached'] else '❌'}")
    print(f"   Final Total: {result['total']/1_000_000} ALGO")