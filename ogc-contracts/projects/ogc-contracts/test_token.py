#!/usr/bin/env python3
"""Test OGC token transfers"""

from beaker import sandbox
from algosdk import transaction as tx

def test_token_transfer():
    print("🧪 Testing OGC Token Transfer...")
    
    algod = sandbox.get_algod_client()
    creator, alice = sandbox.get_accounts()[:2]
    sp = algod.suggested_params()
    
    # Get asset ID from user
    asset_id = int(input("Enter Asset ID from create_ogc_token.py: "))
    
    # Alice opts into the token
    print("📝 Alice opting into OGC token...")
    optin = tx.AssetTransferTxn(
        sender=alice.address,
        sp=sp,
        receiver=alice.address,
        amt=0,
        index=asset_id
    )
    algod.send_transaction(optin.sign(alice.private_key))
    import time
    time.sleep(2)  # Wait for opt-in to confirm
    print("✅ Alice opted in")
    
    # Creator sends tokens to Alice
    print("💸 Sending 1000 OGC to Alice...")
    transfer = tx.AssetTransferTxn(
        sender=creator.address,
        sp=sp,
        receiver=alice.address,
        amt=1000_000_000,  # 1000 OGC (6 decimals)
        index=asset_id
    )
    algod.send_transaction(transfer.sign(creator.private_key))
    print("✅ Transfer complete!")
    
    # Check Alice's balance
    alice_info = algod.account_info(alice.address)
    for asset in alice_info.get("assets", []):
        if asset["asset-id"] == asset_id:
            balance = asset["amount"] / 1_000_000  # Convert from micro-units
            print(f"💰 Alice's OGC balance: {balance} OGC")
            break
    
    print("🎉 Token test successful!")

if __name__ == "__main__":
    test_token_transfer()