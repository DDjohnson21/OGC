#!/usr/bin/env python3
"""
Interact with OGC Token - Transfer, opt-in, check balances
"""

import json
import os
from algosdk.v2client import algod
from algosdk import transaction, encoding
from wallet_selector import select_wallet

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def load_token_info():
    """Load OGC token info"""
    if not os.path.exists("ogc_token_info.json"):
        print("❌ No ogc_token_info.json found")
        print("Create token first: python create_ogc_token.py")
        return None
    
    with open("ogc_token_info.json", 'r') as f:
        return json.load(f)

def opt_in_to_token():
    """Opt into OGC token"""
    token_info = load_token_info()
    if not token_info:
        return
    
    print("🔗 Opt into OGC Token")
    print(f"   Asset ID: {token_info['assetId']}")
    
    # Select wallet
    account = select_wallet()
    if not account:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create opt-in transaction (0 amount to self)
    txn = transaction.AssetTransferTxn(
        sender=account['addr'],
        sp=sp,
        receiver=account['addr'],
        amt=0,
        index=token_info['assetId']
    )
    
    # Sign transaction
    signed_txn = txn.sign(account['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Sent opt-in tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ {account['name']} opted into OGC token!")
        
    except Exception as e:
        print(f"❌ Opt-in failed: {e}")

def transfer_tokens():
    """Transfer OGC tokens"""
    token_info = load_token_info()
    if not token_info:
        return
    
    print("📤 Transfer OGC Tokens")
    print(f"   Asset ID: {token_info['assetId']}")
    
    # Select sender wallet
    sender = select_wallet()
    if not sender:
        return
    
    # Get recipient and amount
    recipient = input("Recipient address: ").strip()
    
    # Validate recipient address
    if not encoding.is_valid_address(recipient):
        print("❌ Invalid recipient address")
        return
    
    amount = float(input(f"Amount to send ({token_info['unitName']}): "))
    # Convert to smallest unit (considering decimals)
    amount_micro = int(amount * (10 ** token_info['decimals']))
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    # Get suggested parameters
    sp = algod_client.suggested_params()
    
    # Create transfer transaction
    txn = transaction.AssetTransferTxn(
        sender=sender['addr'],
        sp=sp,
        receiver=recipient,
        amt=amount_micro,
        index=token_info['assetId']
    )
    
    # Sign transaction
    signed_txn = txn.sign(sender['sk'])
    
    try:
        # Send transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"Sent transfer tx: {tx_id}")
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print(f"✅ Sent {amount} {token_info['unitName']} to {recipient}")
        print(f"   TX: https://testnet.algoexplorer.io/tx/{tx_id}")
        
    except Exception as e:
        print(f"❌ Transfer failed: {e}")

def check_token_balance():
    """Check OGC token balance"""
    token_info = load_token_info()
    if not token_info:
        return
    
    print("💰 Check OGC Token Balance")
    
    # Select wallet
    account = select_wallet()
    if not account:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    try:
        account_info = algod_client.account_info(account['addr'])
        assets = account_info.get('assets', [])
        
        # Find OGC token
        ogc_balance = 0
        opted_in = False
        
        for asset in assets:
            if asset['asset-id'] == token_info['assetId']:
                ogc_balance = asset['amount']
                opted_in = True
                break
        
        print(f"📊 {account['name']} Token Balance:")
        print(f"   Address: {account['addr']}")
        
        if opted_in:
            # Convert from micro units
            balance_display = ogc_balance / (10 ** token_info['decimals'])
            print(f"   OGC Balance: {balance_display:,.6f} {token_info['unitName']}")
        else:
            print(f"   ❌ Not opted into OGC token")
            print(f"   Use option 1 to opt in first")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{account['addr']}")
        
    except Exception as e:
        print(f"❌ Could not check balance: {e}")

def main():
    """Main interaction menu"""
    while True:
        print("\n🪙 OGC Token Interaction")
        print("1. Opt into OGC token")
        print("2. Transfer OGC tokens")
        print("3. Check token balance")
        print("4. Show token info")
        print("5. Exit")
        
        choice = input("Choose (1-5): ").strip()
        
        if choice == "1":
            opt_in_to_token()
        elif choice == "2":
            transfer_tokens()
        elif choice == "3":
            check_token_balance()
        elif choice == "4":
            token_info = load_token_info()
            if token_info:
                print(f"\n🪙 OGC Token Info:")
                print(f"   Asset ID: {token_info['assetId']}")
                print(f"   Name: {token_info['name']}")
                print(f"   Symbol: {token_info['unitName']}")
                print(f"   Total: {token_info['total']:,}")
                print(f"   Asset: https://testnet.algoexplorer.io/asset/{token_info['assetId']}")
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()