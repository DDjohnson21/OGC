#!/usr/bin/env python3
"""
Create OGC Token (ASA) - Inherits wallet system from existing branch
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def create_ogc_token():
    """Create OGC token (ASA)"""
    print("🪙 Create OGC Token")
    
    # Select wallet
    creator = select_wallet()
    if not creator:
        print("❌ No wallet selected")
        return
    
    # Token parameters
    print(f"\n📋 Token Configuration:")
    total_supply = 1_000_000_000  # 1 billion tokens
    decimals = 6
    unit_name = "OGC"
    asset_name = "OGC Token"
    
    print(f"   Name: {asset_name}")
    print(f"   Symbol: {unit_name}")
    print(f"   Total Supply: {total_supply:,}")
    print(f"   Decimals: {decimals}")
    print(f"   Creator: {creator['addr']}")
    
    confirm = input("\nCreate token? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled")
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create asset creation transaction
    txn = transaction.AssetCreateTxn(
        sender=creator['addr'],
        sp=sp,
        total=total_supply,
        decimals=decimals,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=creator['addr'],
        reserve=creator['addr'],
        freeze=None,
        clawback=None,
        url="https://github.com/DDjohnson21/OGC",
        metadata_hash=None
    )
    
    # Sign transaction
    signed_txn = txn.sign(creator['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Sent asset create tx: {tx_id}")
        
        # Wait for confirmation
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        asset_id = confirmed_txn["asset-index"]
        
        if not asset_id:
            raise ValueError("No asset-index in create confirmation!")
        
        print(f"\n✅ OGC Token Created!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Total Supply: {total_supply:,} {unit_name}")
        print(f"   Creator: {creator['addr']}")
        print(f"   Created by: {creator['name']}")
        
        # Save token info
        token_info = {
            "assetId": asset_id,
            "name": asset_name,
            "unitName": unit_name,
            "total": total_supply,
            "decimals": decimals,
            "creator": creator['addr'],
            "network": "testnet",
            "createdBy": creator['name'],
            "txId": tx_id
        }
        
        with open("ogc_token_info.json", 'w') as f:
            json.dump(token_info, f, indent=2)
        
        print(f"Wrote ogc_token_info.json")
        
        print(f"\n🔗 Links:")
        print(f"   TX: https://testnet.algoexplorer.io/tx/{tx_id}")
        print(f"   Asset: https://testnet.algoexplorer.io/asset/{asset_id}")
        
        print(f"\n💡 Use Asset ID {asset_id} in your demos!")
        
        return asset_id
        
    except Exception as e:
        print(f"❌ Token creation failed: {e}")
        return None

def check_ogc_token():
    """Check existing OGC token info"""
    if not os.path.exists("ogc_token_info.json"):
        print("❌ No ogc_token_info.json found")
        print("Create token first: python create_ogc_token.py")
        return
    
    with open("ogc_token_info.json", 'r') as f:
        token_info = json.load(f)
    
    print("🪙 OGC Token Info")
    print(f"   Asset ID: {token_info['assetId']}")
    print(f"   Name: {token_info['name']}")
    print(f"   Symbol: {token_info['unitName']}")
    print(f"   Total Supply: {token_info['total']:,}")
    print(f"   Decimals: {token_info['decimals']}")
    print(f"   Creator: {token_info['creator']}")
    print(f"   Created by: {token_info['createdBy']}")
    
    print(f"\n🔗 Links:")
    print(f"   Asset: https://testnet.algoexplorer.io/asset/{token_info['assetId']}")
    
    # Check if token exists on chain
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    try:
        asset_info = algod_client.asset_info(token_info['assetId'])
        params = asset_info["params"]
        
        print(f"\n✅ Token verified on TestNet:")
        print(f"   On-chain name: {params['name']}")
        print(f"   On-chain symbol: {params['unit-name']}")
        print(f"   On-chain total: {params['total']:,}")
        
    except Exception as e:
        print(f"\n❌ Could not verify token on chain: {e}")

def main():
    """Main menu"""
    while True:
        print("\n🪙 OGC Token Management")
        print("1. Create OGC token")
        print("2. Check existing token")
        print("3. Exit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            create_ogc_token()
        elif choice == "2":
            check_ogc_token()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()