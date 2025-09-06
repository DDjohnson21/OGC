#!/usr/bin/env python3
"""
OGC - Out The Groupchat Demo
Hackathon project showcasing decentralized group funding on Algorand
"""

from beaker import sandbox, client
from working_vault import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner
import time

def ogc_demo():
    print("🚀 OGC - Out The Groupchat")
    print("=" * 50)
    print("Decentralized Group Funding on Algorand")
    print("Hackathon Demo\n")
    
    # Simulate group chat scenario
    print("💬 Scenario: Group Chat Planning")
    print("   'Hey guys, let's go to that concert!'")
    print("   'I'm in if we get 10 people'")
    print("   'Same, but I need commitment first'")
    print("   'Let's use OGC to collect funds!'")
    print()
    
    # Setup
    algod_client = sandbox.get_algod_client()
    organizer = sandbox.get_accounts().pop()
    alice = sandbox.get_accounts().pop()
    bob = sandbox.get_accounts().pop()
    charlie = sandbox.get_accounts().pop()
    
    # Concert ticket scenario
    ticket_price = 50_000_000  # 50 ALGO total for group tickets
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 20  # 20 rounds to decide
    
    print(f"🎫 Creating Concert Fund:")
    print(f"   Organizer: {organizer.address[:10]}...")
    print(f"   Target: {ticket_price/1_000_000} ALGO")
    print(f"   Deadline: {deadline_round - current_round} rounds")
    
    # Deploy vault
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=organizer.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=ticket_price,
        deadline_round=deadline_round,
        receiver_addr=organizer.address,  # Organizer handles ticket purchase
    )
    
    print(f"   ✅ Fund Created: APP_ID {app_id}")
    
    # Fund app for operations
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(organizer.address, sp, app_addr, 5_000_000)
    algod_client.send_transaction(fund_txn.sign(organizer.private_key))
    
    print(f"\n💰 Group Members Contributing:")
    
    # Alice contributes
    alice_amount = 15_000_000  # 15 ALGO
    print(f"   Alice: 'I'm in!' - Contributing {alice_amount/1_000_000} ALGO")
    
    pmt_alice = tx.PaymentTxn(alice.address, sp, app_addr, alice_amount)
    pmt_alice_signed = TransactionWithSigner(pmt_alice, alice.signer)
    
    app_client_alice = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=alice.signer
    )
    app_client_alice.call("contribute", payment=pmt_alice_signed)
    
    total_after_alice = app_client.call("get_total").return_value
    print(f"   💳 Total: {total_after_alice/1_000_000} ALGO")
    
    # Bob contributes
    bob_amount = 20_000_000  # 20 ALGO
    print(f"   Bob: 'Count me in!' - Contributing {bob_amount/1_000_000} ALGO")
    
    pmt_bob = tx.PaymentTxn(bob.address, sp, app_addr, bob_amount)
    pmt_bob_signed = TransactionWithSigner(pmt_bob, bob.signer)
    
    app_client_bob = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=bob.signer
    )
    app_client_bob.call("contribute", payment=pmt_bob_signed)
    
    total_after_bob = app_client.call("get_total").return_value
    print(f"   💳 Total: {total_after_bob/1_000_000} ALGO")
    
    # Charlie contributes
    charlie_amount = 15_000_000  # 15 ALGO
    print(f"   Charlie: 'Let's do this!' - Contributing {charlie_amount/1_000_000} ALGO")
    
    pmt_charlie = tx.PaymentTxn(charlie.address, sp, app_addr, charlie_amount)
    pmt_charlie_signed = TransactionWithSigner(pmt_charlie, charlie.signer)
    
    app_client_charlie = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=charlie.signer
    )
    app_client_charlie.call("contribute", payment=pmt_charlie_signed)
    
    final_total = app_client.call("get_total").return_value
    goal = app_client.call("get_goal").return_value
    
    print(f"   💳 Final Total: {final_total/1_000_000} ALGO")
    print(f"   🎯 Goal: {goal/1_000_000} ALGO")
    
    # Check if goal reached
    if final_total >= goal:
        print(f"\n🎉 SUCCESS! Goal Reached!")
        print(f"   'We did it! Concert tickets secured!'")
        print(f"   'OGC made this so easy and trustless!'")
        
        # Simulate waiting for deadline
        print(f"\n⏰ Waiting for deadline to release funds...")
        current_round = algod_client.status()["last-round"]
        
        if current_round >= deadline_round:
            print(f"   ✅ Deadline reached - releasing funds")
            try:
                organizer_balance_before = algod_client.account_info(organizer.address)["amount"]
                app_client.call("release")
                organizer_balance_after = algod_client.account_info(organizer.address)["amount"]
                received = organizer_balance_after - organizer_balance_before
                print(f"   💰 Organizer received {received/1_000_000} ALGO")
                print(f"   🎫 'Buying tickets now!'")
            except Exception as e:
                print(f"   ⚠️ Release will work after deadline: {e}")
        else:
            print(f"   ⏳ {deadline_round - current_round} rounds until release")
    else:
        needed = goal - final_total
        print(f"\n😔 Goal not reached - need {needed/1_000_000} more ALGO")
        print(f"   'Maybe next time... at least our funds are safe!'")
    
    print(f"\n🏆 OGC Demo Complete!")
    print(f"   Smart Contract: {app_id}")
    print(f"   Trustless: ✅ No central authority")
    print(f"   Transparent: ✅ All transactions on-chain")
    print(f"   Secure: ✅ Funds locked until goal/deadline")
    print(f"   Decentralized: ✅ Runs on Algorand")
    
    return {
        "app_id": app_id,
        "total_raised": final_total,
        "goal": goal,
        "success": final_total >= goal
    }

if __name__ == "__main__":
    result = ogc_demo()
    print(f"\n📊 Final Stats:")
    print(f"   Raised: {result['total_raised']/1_000_000} ALGO")
    print(f"   Success: {'🎉' if result['success'] else '😔'}")