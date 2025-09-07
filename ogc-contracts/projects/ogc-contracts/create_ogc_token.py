#!/usr/bin/env python3
"""Create OGC Token (ASA) for demo"""

from beaker import sandbox
from algosdk import transaction as tx

def create_ogc_token():
    print("🪙 Creating OGC Token...")
    
    algod = sandbox.get_algod_client()
    creator = sandbox.get_accounts().pop()
    sp = algod.suggested_params()
    
    # Create ASA
    txn = tx.AssetCreateTxn(
        sender=creator.address,
        sp=sp,
        total=1_000_000_000,       # 1 billion tokens
        decimals=6,                # 6 decimal places
        default_frozen=False,
        unit_name="OGC",
        asset_name="OGC Token",
        url="https://ogc.example.com",
        manager=creator.address,
        reserve=creator.address,
        freeze=None,
        clawback=None,
    )
    
    stx = txn.sign(creator.private_key)
    txid = algod.send_transaction(stx)
    
    # Wait for confirmation
    import time
    time.sleep(2)  # Simple wait
    confirmed = algod.pending_transaction_info(txid)
    asset_id = confirmed["asset-index"]
    
    print(f"✅ OGC Token Created!")
    print(f"   Asset ID: {asset_id}")
    print(f"   Total Supply: 1,000,000,000 OGC")
    print(f"   Creator: {creator.address}")
    
    return asset_id, creator

if __name__ == "__main__":
    asset_id, creator = create_ogc_token()
    print(f"\n💡 Use Asset ID {asset_id} in your demos!")