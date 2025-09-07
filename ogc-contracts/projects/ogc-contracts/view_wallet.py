#!/usr/bin/env python3
"""View saved wallet details"""

def view_wallet():
    print("🔐 Your Saved TestNet Wallet")
    print("=" * 50)
    
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    address = os.getenv('TESTNET_ADDRESS', 'Not found in .env')
    mnemonic = os.getenv('TESTNET_MNEMONIC', 'Not found in .env')
    
    print(f"Address: {address}")
    print(f"\nMnemonic (25 words):")
    print(f"{mnemonic}")
    
    print(f"\n🔗 Links:")
    print(f"TestNet Explorer: https://testnet.algoexplorer.io/address/{address}")
    print(f"Get TestNet ALGO: https://testnet.algoexplorer.io/dispenser")
    
    print(f"\n📱 Import to Pera Wallet:")
    print(f"1. Open Pera Wallet")
    print(f"2. Add Account → Import Account")
    print(f"3. Enter the 25-word mnemonic above")
    print(f"4. Switch to TestNet")
    
    print(f"\n⚠️  SECURITY:")
    print(f"- This is for TestNet only (no real value)")
    print(f"- Never share MainNet mnemonics")
    print(f"- Keep this safe for your demos")

if __name__ == "__main__":
    view_wallet()