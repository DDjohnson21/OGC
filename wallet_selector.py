#!/usr/bin/env python3
"""
Wallet selector utility - choose between multiple wallets
"""

import json
import os
from algosdk import mnemonic, account

WALLETS_PATH = os.path.join(os.path.dirname(__file__), "wallets.json")

def load_wallets():
    """Load all available wallets"""
    with open(WALLETS_PATH, 'r') as f:
        return json.load(f)

def select_wallet():
    """Interactive wallet selection"""
    wallets = load_wallets()
    
    print("💳 Available Wallets:")
    wallet_keys = list(wallets.keys())
    
    for i, key in enumerate(wallet_keys, 1):
        wallet = wallets[key]
        print(f"{i}. {key}: {wallet['addr']} ({wallet.get('note', 'no note')})")
    
    while True:
        try:
            choice = int(input(f"Choose wallet (1-{len(wallet_keys)}): ")) - 1
            if 0 <= choice < len(wallet_keys):
                selected_key = wallet_keys[choice]
                selected_wallet = wallets[selected_key]
                
                # Validate mnemonic if provided
                if selected_wallet['mnemonic'] != "YOUR_24_OR_25_WORD_MNEMONIC_HERE":
                    try:
                        private_key = mnemonic.to_private_key(selected_wallet['mnemonic'])
                        derived_addr = account.address_from_private_key(private_key)
                        
                        print(f"✅ Selected: {selected_key}")
                        print(f"   Address: {selected_wallet['addr']}")
                        
                        if derived_addr != selected_wallet['addr']:
                            print(f"⚠️  Warning: Mnemonic doesn't match address!")
                        
                        return {
                            "addr": selected_wallet['addr'],
                            "sk": private_key,
                            "name": selected_key
                        }
                    except Exception as e:
                        print(f"❌ Invalid mnemonic for {selected_key}: {e}")
                        continue
                else:
                    print(f"❌ Please update mnemonic for {selected_key} in wallets.json")
                    continue
            else:
                print("❌ Invalid choice")
        except ValueError:
            print("❌ Please enter a number")

def get_wallet_by_name(name):
    """Get specific wallet by name"""
    wallets = load_wallets()
    if name not in wallets:
        raise ValueError(f"Wallet '{name}' not found")
    
    wallet = wallets[name]
    private_key = mnemonic.to_private_key(wallet['mnemonic'])
    
    return {
        "addr": wallet['addr'],
        "sk": private_key,
        "name": name
    }

if __name__ == "__main__":
    wallet = select_wallet()
    if wallet:
        print(f"Selected wallet: {wallet['name']} - {wallet['addr']}")