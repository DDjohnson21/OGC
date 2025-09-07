#!/usr/bin/env python3
"""Send ALGO - supports both wallet formats"""

from algosdk.v2client import algod
from algosdk import mnemonic, transaction as tx, account
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def flexible_send():
    print("📤 Flexible ALGO Sender")
    print("Works with Universal (24-word) and Legacy (25-word) wallets")
    
    print("\n1. Use saved Legacy wallet (25-word)")
    print("2. Enter your mnemonic (24 or 25 words)")
    print("3. Create new Legacy wallet")
    
    choice = input("Choose (1, 2, or 3): ").strip()
    
    if choice == "1":
        # Use saved Legacy wallet from environment
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        mnemo = os.getenv('TESTNET_MNEMONIC')
        if not mnemo:
            print("❌ TESTNET_MNEMONIC not found in .env file")
            return
        sk = mnemonic.to_private_key(mnemo)
        sender_addr = algosdk.account.address_from_private_key(sk)
        print(f"Using saved wallet: {sender_addr}")
        
    elif choice == "2":
        # Try user's mnemonic
        user_mnemonic = input("Paste your mnemonic: ").strip()
        words = user_mnemonic.split()
        
        if len(words) == 24:
            print("❌ Universal (24-word) format detected")
            print("Python SDK requires Legacy (25-word) format")
            print("Options:")
            print("- Use WalletConnect integration")
            print("- Create Legacy wallet (option 3)")
            print("- Import Legacy wallet to Pera")
            return
            
        elif len(words) == 25:
            try:
                sk = mnemonic.to_private_key(user_mnemonic)
                sender_addr = algosdk.account.address_from_private_key(sk)
                print(f"✅ Legacy wallet detected: {sender_addr}")
            except Exception as e:
                print(f"❌ Invalid mnemonic: {e}")
                return
        else:
            print(f"❌ Invalid: Expected 24 or 25 words, got {len(words)}")
            return
            
    elif choice == "3":
        # Create new Legacy wallet
        print("Creating new Legacy wallet...")
        sk, sender_addr = account.generate_account()
        mnemo = mnemonic.from_private_key(sk)
        
        print(f"✅ New Legacy Wallet:")
        print(f"   Address: {sender_addr}")
        print(f"   Mnemonic: {mnemo}")
        print(f"   Save this for future use!")
        
        use_new = input("Use this wallet now? (y/N): ").strip().lower()
        if use_new != 'y':
            return
    else:
        print("❌ Invalid choice")
        return
    
    # Continue with sending
    recipient = input("Recipient address: ").strip()
    amount_algo = float(input("Amount (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    algod_client = algod.AlgodClient("", ALGOD_URL, "")
    
    try:
        # Check balance
        info = algod_client.account_info(sender_addr)
        balance = info["amount"] / 1_000_000
        print(f"Balance: {balance} ALGO")
        
        if balance < amount_algo + 0.001:
            print(f"❌ Insufficient balance")
            return
        
        # Send transaction
        sp = algod_client.suggested_params()
        txn = tx.PaymentTxn(sender_addr, sp, recipient, amount_micro)
        stx = txn.sign(sk)
        txid = algod_client.send_transaction(stx)
        
        print(f"✅ Sent {amount_algo} ALGO to {recipient}")
        print(f"TX: https://testnet.algoexplorer.io/tx/{txid}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    flexible_send()