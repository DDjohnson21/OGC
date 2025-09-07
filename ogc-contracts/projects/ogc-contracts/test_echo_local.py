#!/usr/bin/env python3
"""Test Echo Contract Locally"""

from beaker import sandbox, client
from echo_contract import app
from algosdk import transaction as tx
from algosdk.atomic_transaction_composer import TransactionWithSigner

def test_echo_contract():
    print("🔄 Testing Echo Contract Locally")
    
    algod_client = sandbox.get_algod_client()
    deployer = sandbox.get_accounts().pop()
    sender = sandbox.get_accounts().pop()
    
    # Deploy contract
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=deployer.signer,
    )
    
    app_id, app_addr, _ = app_client.create()
    print(f"✅ Echo Contract Deployed: APP_ID {app_id}")
    print(f"   Address: {app_addr}")
    
    # Fund the contract so it can send ALGO back
    sp = algod_client.suggested_params()
    fund_txn = tx.PaymentTxn(deployer.address, sp, app_addr, 5_000_000)  # 5 ALGO
    algod_client.send_transaction(fund_txn.sign(deployer.private_key))
    print(f"✅ Contract funded with 5 ALGO")
    
    # Test: Send 1 ALGO to contract
    test_amount = 1_000_000  # 1 ALGO
    print(f"\n🧪 Test: Sending {test_amount/1_000_000} ALGO to contract...")
    
    # Get sender's balance before
    sender_balance_before = algod_client.account_info(sender.address)["amount"]
    
    # Send payment to contract
    payment = tx.PaymentTxn(sender.address, sp, app_addr, test_amount)
    payment_signed = TransactionWithSigner(payment, sender.signer)
    
    # Call echo_payment method
    app_client_sender = client.ApplicationClient(
        client=algod_client, app=app, app_id=app_id, signer=sender.signer
    )
    
    try:
        app_client_sender.call("echo_payment", payment=payment_signed)
        print("✅ Echo payment successful!")
        
        # Check sender's balance after
        sender_balance_after = algod_client.account_info(sender.address)["amount"]
        difference = (sender_balance_after - sender_balance_before) / 1_000_000
        
        print(f"📊 Results:")
        print(f"   Sent: {test_amount/1_000_000} ALGO")
        print(f"   Net change: {difference} ALGO (should be ~-0.002 for fees)")
        
        # Check contract stats
        total = app_client.call("get_total").return_value
        print(f"   Contract total received: {total/1_000_000} ALGO")
        
        print(f"\n🎉 SUCCESS! Contract automatically sent ALGO back!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_echo_contract()