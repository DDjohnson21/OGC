#!/usr/bin/env python3
"""
Simple Reusable Wallet Manager

Creates and manages a permanent wallet address for ALGO transactions.
"""

import json
import os
import sys
from datetime import datetime
from algosdk.v2client import algod
from algosdk import mnemonic, account, transaction
from algosdk.transaction import PaymentTxn

# Algorand Testnet configuration
ALGOD_TOKEN = ""
ALGOD_SERVER = "https://testnet-api.algonode.cloud"

# Create Algod client
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_SERVER)

WALLET_FILE = "permanent_wallet.json"


def create_permanent_wallet():
    """Create a new permanent wallet"""
    print("🔑 Creating permanent wallet...")
    
    # Generate new account
    private_key, address = account.generate_account()
    wallet_mnemonic = mnemonic.from_private_key(private_key)
    
    wallet = {
        "address": address,
        "mnemonic": wallet_mnemonic,
        "privateKey": list(private_key),
        "createdAt": datetime.now().isoformat(),
        "type": "permanent"
    }
    
    # Save wallet to file
    with open(WALLET_FILE, 'w') as f:
        json.dump(wallet, f, indent=2)
    
    print("✅ Permanent wallet created!")
    print(f"📍 Address: {address}")
    print(f"🔐 Mnemonic: {wallet_mnemonic}")
    print(f"💾 Saved to: {WALLET_FILE}")
    print("\n⚠️  IMPORTANT: Save this mnemonic safely!")
    print("   This is your permanent wallet address.")
    
    return wallet


def load_permanent_wallet():
    """Load permanent wallet from file or create new one"""
    if not os.path.exists(WALLET_FILE):
        print("❌ No permanent wallet found. Creating new one...")
        return create_permanent_wallet()
    
    try:
        with open(WALLET_FILE, 'r') as f:
            wallet = json.load(f)
        
        # Handle different wallet file formats
        address = wallet.get('address') or wallet.get('addr')
        created_at = wallet.get('createdAt') or wallet.get('note', 'Unknown')
        
        print("✅ Permanent wallet loaded!")
        print(f"📍 Address: {address}")
        print(f"📅 Created: {created_at}")
        
        # Normalize wallet format
        return {
            "address": address,
            "addr": address,  # Keep both for compatibility
            "mnemonic": wallet['mnemonic'],
            "privateKey": wallet.get('privateKey'),
            "createdAt": created_at,
            "type": wallet.get('type', 'permanent')
        }
    
    except Exception as error:
        print("❌ Error loading wallet. Creating new one...")
        return create_permanent_wallet()


def get_account_from_wallet(wallet):
    """Get account object from wallet"""
    # If we have privateKey array, use it; otherwise derive from mnemonic
    if wallet.get('privateKey') and isinstance(wallet['privateKey'], list):
        private_key = bytes(wallet['privateKey'])
    elif wallet.get('mnemonic'):
        private_key = mnemonic.to_private_key(wallet['mnemonic'])
    else:
        raise ValueError('No private key or mnemonic found in wallet')
    
    return {
        "addr": wallet.get('address') or wallet.get('addr'),
        "sk": private_key
    }


def check_balance(address):
    """Check account balance"""
    try:
        account_info = algod_client.account_info(address)
        balance = account_info['amount'] / 1e6
        return balance
    except Exception as error:
        print(f"❌ Error checking balance: {error}")
        return 0


def fund_wallet(wallet):
    """Show funding instructions"""
    print("\n💰 Wallet Funding Instructions:")
    print(f"📍 Your permanent wallet address: {wallet['address']}")
    print("🔗 Go to: https://testnet.algoexplorer.io/dispenser")
    print("📝 Copy and paste your address above")
    print("💵 Request at least 10 ALGO (it's free!)")
    print("⏳ Press Enter when you have funded the wallet...")
    
    input()  # Wait for user input
    
    balance = check_balance(wallet['address'])
    print(f"✅ Wallet balance: {balance} ALGO")
    
    if balance < 1:
        print("⚠️  Low balance! Please fund your wallet.")
        return False
    
    return True


def send_algo(from_wallet, to_address, amount):
    """Send ALGO to another address"""
    try:
        print(f"\n💸 Sending {amount} ALGO to {to_address}...")
        
        account_obj = get_account_from_wallet(from_wallet)
        sp = algod_client.suggested_params()
        
        # Create payment transaction
        txn = PaymentTxn(
            sender=account_obj['addr'],
            sp=sp,
            receiver=to_address,
            amt=int(amount * 1e6)  # Convert to microALGO
        )
        
        # Sign transaction
        signed_txn = txn.sign(account_obj['sk'])
        
        # Send transaction
        tx_id = algod_client.send_transaction(signed_txn)
        print(f"📤 Transaction sent: {tx_id}")
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(algod_client, tx_id, 4)
        print("✅ Transaction confirmed!")
        
        return tx_id
    
    except Exception as error:
        print(f"❌ Error sending ALGO: {error}")
        raise error


def main():
    """Main function"""
    try:
        print("🌟 Simple Reusable Wallet Manager\n")
        
        # Load or create permanent wallet
        wallet = load_permanent_wallet()
        
        # Check current balance
        balance = check_balance(wallet['address'])
        print(f"💰 Current balance: {balance} ALGO")
        
        if balance < 1:
            print("\n💳 Wallet needs funding...")
            funded = fund_wallet(wallet)
            if not funded:
                print("❌ Please fund your wallet first.")
                return
        
        print("\n🎯 Your Permanent Wallet:")
        print(f"📍 Address: {wallet['address']}")
        print(f"💰 Balance: {check_balance(wallet['address'])} ALGO")
        
        print("\n📋 Available Commands:")
        print("1. Check balance: python simple_wallet.py balance")
        print("2. Send ALGO: python simple_wallet.py send <address> <amount>")
        print("3. Fund wallet: python simple_wallet.py fund")
        
        # Handle command line arguments
        args = sys.argv[1:]
        
        if len(args) == 0:
            print("\n💡 Usage:")
            print("  python simple_wallet.py balance")
            print("  python simple_wallet.py send <address> <amount>")
            print("  python simple_wallet.py fund")
        elif args[0] == "balance":
            balance = check_balance(wallet['address'])
            print(f"💰 Balance: {balance} ALGO")
        elif args[0] == "send" and len(args) >= 3:
            to_address = args[1]
            amount = float(args[2])
            send_algo(wallet, to_address, amount)
        elif args[0] == "fund":
            fund_wallet(wallet)
        else:
            print("\n💡 Usage:")
            print("  python simple_wallet.py balance")
            print("  python simple_wallet.py send <address> <amount>")
            print("  python simple_wallet.py fund")
    
    except Exception as error:
        print(f"❌ Error: {error}")


if __name__ == "__main__":
    main()
