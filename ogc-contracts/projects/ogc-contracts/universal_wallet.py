#!/usr/bin/env python3
"""Handle both Universal (24-word) and Legacy (25-word) wallets"""

from algosdk import mnemonic, account
import algosdk

def detect_wallet_type():
    print("🔍 Wallet Format Detector")
    print("1. Test your mnemonic")
    print("2. Create Legacy wallet (25-word)")
    print("3. View saved Legacy wallet")
    
    choice = input("Choose (1, 2, or 3): ").strip()
    
    if choice == "1":
        # Test user's mnemonic
        user_mnemonic = input("Paste your mnemonic: ").strip()
        words = user_mnemonic.split()
        
        print(f"\n📊 Analysis:")
        print(f"   Word count: {len(words)}")
        
        if len(words) == 24:
            print("   Format: Universal (24-word)")
            print("   ⚠️  Python SDK needs 25-word Legacy format")
            print("   💡 Use WalletConnect or create Legacy wallet")
            
        elif len(words) == 25:
            print("   Format: Legacy (25-word)")
            try:
                sk = mnemonic.to_private_key(user_mnemonic)
                addr = algosdk.account.address_from_private_key(sk)
                print(f"   ✅ Valid! Address: {addr}")
            except Exception as e:
                print(f"   ❌ Invalid: {e}")
                
        else:
            print(f"   ❌ Invalid: Expected 24 or 25 words, got {len(words)}")
    
    elif choice == "2":
        # Create new Legacy wallet
        print("\n🔑 Creating Legacy Wallet (25-word)...")
        sk, addr = account.generate_account()
        mnemo = mnemonic.from_private_key(sk)
        
        print(f"✅ Legacy Wallet Created:")
        print(f"   Address: {addr}")
        print(f"   Mnemonic: {mnemo}")
        print(f"   Words: {len(mnemo.split())}")
        print(f"   Compatible with Python SDK: ✅")
        
    elif choice == "3":
        # Show saved Legacy wallet
        address = "ZHMX3URT56ZLWQY3Y74CRXVOAVEOELOAVMXJZDT76IFORLPWMWMPJVAEN4"
        mnemo = "swear suffer shrimp clinic cause differ nice space update mansion cradle brisk unknown lecture host clarify again faint divide decrease renew choice still abstract tomorrow"
        
        print(f"\n🔐 Saved Legacy Wallet:")
        print(f"   Address: {address}")
        print(f"   Mnemonic: {mnemo}")
        print(f"   Words: {len(mnemo.split())}")
        print(f"   Format: Legacy (Python SDK compatible)")
        
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    detect_wallet_type()