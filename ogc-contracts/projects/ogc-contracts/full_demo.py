#!/usr/bin/env python3
"""Full OGC Demo - ALGO Vault + Token Creation"""

from beaker import sandbox, client
from working_vault import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner
import time

def full_ogc_demo():
    print("🚀 OGC - Complete Demo")
    print("=" * 50)
    
    algod_client = sandbox.get_algod_client()
    organizer = sandbox.get_accounts().pop()
    alice = sandbox.get_accounts().pop()
    bob = sandbox.get_accounts().pop()
    
    # Part 1: Create OGC Token
    print("\n🪙 Part 1: Creating OGC Token")
    sp = algod_client.suggested_params()
    
    token_txn = tx.AssetCreateTxn(
        sender=organizer.address,
        sp=sp,
        total=1_000_000_000,
        decimals=6,
        default_frozen=False,
        unit_name="OGC",
        asset_name="OGC Token",
        manager=organizer.address,
        reserve=organizer.address,
        freeze=None,
        clawback=None,
    )
    
    stx = token_txn.sign(organizer.private_key)
    txid = algod_client.send_transaction(stx)
    time.sleep(2)
    confirmed = algod_client.pending_transaction_info(txid)
    asset_id = confirmed["asset-index"]
    
    print(f"✅ OGC Token Created: Asset ID {asset_id}")
    
    # Part 2: ALGO Vault Demo
    print(f"\n💰 Part 2: ALGO Vault Demo")
    goal = 5_000_000  # 5 ALGO
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 100
    
    print(f"🎯 Goal: {goal/1_000_000} ALGO")
    
    # Deploy vault
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
    
    print(f"✅ Vault Deployed: APP_ID {app_id}")
    
    # Fund app for operations
    fund_txn = tx.PaymentTxn(organizer.address, sp, app_addr, 3_000_000)
    algod_client.send_transaction(fund_txn.sign(organizer.private_key))
    
    # Alice contributes 2 ALGO
    alice_amount = 2_000_000
    print(f"👤 Alice contributes {alice_amount/1_000_000} ALGO")
    
    pmt_alice = tx.PaymentTxn(alice.address, sp, app_addr, alice_amount)
    pmt_alice_signed = TransactionWithSigner(pmt_alice, alice.signer)
    
    app_client_alice = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=alice.signer
    )
    app_client_alice.call("contribute", payment=pmt_alice_signed)
    
    total_after_alice = app_client.call("get_total").return_value
    print(f"💳 Total after Alice: {total_after_alice/1_000_000} ALGO")
    
    # Bob contributes 3 ALGO
    bob_amount = 3_000_000
    print(f"👤 Bob contributes {bob_amount/1_000_000} ALGO")
    
    pmt_bob = tx.PaymentTxn(bob.address, sp, app_addr, bob_amount)
    pmt_bob_signed = TransactionWithSigner(pmt_bob, bob.signer)
    
    app_client_bob = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=bob.signer
    )
    app_client_bob.call("contribute", payment=pmt_bob_signed)
    
    final_total = app_client.call("get_total").return_value
    goal_amount = app_client.call("get_goal").return_value
    
    print(f"💳 Final Total: {final_total/1_000_000} ALGO")
    print(f"🎯 Goal: {goal_amount/1_000_000} ALGO")
    
    if final_total >= goal_amount:
        print(f"🎉 SUCCESS! Goal Reached!")
        print(f"   Ready to release funds after deadline")
    else:
        needed = goal_amount - final_total
        print(f"⏳ Need {needed/1_000_000} more ALGO")
    
    # Part 3: Token Info
    print(f"\n🪙 Part 3: Token Summary")
    try:
        asset_info = algod_client.asset_info(asset_id)
        params = asset_info["params"]
        print(f"✅ Token Details:")
        print(f"   Name: {params['name']}")
        print(f"   Symbol: {params['unit-name']}")
        print(f"   Total Supply: {params['total']:,}")
        print(f"   Decimals: {params['decimals']}")
    except Exception as e:
        print(f"❌ Token info error: {e}")
    
    print(f"\n🏆 Demo Complete!")
    print(f"   ALGO Vault: APP_ID {app_id}")
    print(f"   OGC Token: Asset ID {asset_id}")
    print(f"   Total Raised: {final_total/1_000_000} ALGO")
    print(f"   Goal Status: {'✅ Reached' if final_total >= goal_amount else '⏳ Pending'}")
    
    return {
        "vault_app_id": app_id,
        "token_asset_id": asset_id,
        "total_raised": final_total,
        "goal": goal_amount,
        "success": final_total >= goal_amount
    }

if __name__ == "__main__":
    result = full_ogc_demo()
    print(f"\n📊 Final Results:")
    print(f"   Vault: {result['vault_app_id']}")
    print(f"   Token: {result['token_asset_id']}")
    print(f"   Success: {'🎉' if result['success'] else '⏳'}")