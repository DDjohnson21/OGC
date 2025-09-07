#!/usr/bin/env python3
"""
Check balance of any address, contract, or wallet
Inherits from existing wallet system
"""

import json
import os
from algosdk.v2client import algod
from algosdk import logic, encoding
from wallet_selector import select_wallet, load_wallets

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def check_wallet_balance():
    """Check balance of a wallet from wallet selector"""
    print("💳 Check Wallet Balance")
    
    # Select wallet
    wallet = select_wallet()
    if not wallet:
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    try:
        account_info = algod_client.account_info(wallet['addr'])
        balance = account_info['amount'] / 1_000_000
        
        print(f"\n💰 {wallet['name']} Balance:")
        print(f"   Address: {wallet['addr']}")
        print(f"   ALGO Balance: {balance} ALGO")
        
        # Check for assets (tokens)
        assets = account_info.get('assets', [])
        if assets:
            print(f"   Assets: {len(assets)} token(s)")
            for asset in assets[:3]:  # Show first 3
                print(f"     Asset {asset['asset-id']}: {asset['amount']}")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{wallet['addr']}")
        
    except Exception as e:
        print(f"❌ Could not check balance: {e}")

def check_address_balance():
    """Check balance of any address"""
    print("📍 Check Any Address Balance")
    
    address = input("Enter address: ").strip()
    
    # Validate address
    if not encoding.is_valid_address(address):
        print("❌ Invalid address format")
        return
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    try:
        account_info = algod_client.account_info(address)
        balance = account_info['amount'] / 1_000_000
        
        print(f"\n💰 Address Balance:")
        print(f"   Address: {address}")
        print(f"   ALGO Balance: {balance} ALGO")
        
        # Check if it's an app account
        if account_info.get('apps-total-schema'):
            print(f"   Type: Smart Contract Account")
        
        # Check for assets
        assets = account_info.get('assets', [])
        if assets:
            print(f"   Assets: {len(assets)} token(s)")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{address}")
        
    except Exception as e:
        print(f"❌ Could not check balance: {e}")

def check_contract_balance():
    """Check balance of a contract by APP_ID"""
    print("🏦 Check Contract Balance")
    
    try:
        app_id = int(input("Enter APP_ID: "))
    except ValueError:
        print("❌ Invalid APP_ID")
        return
    
    # Get contract address
    app_addr = logic.get_application_address(app_id)
    
    # Initialize Algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    try:
        account_info = algod_client.account_info(app_addr)
        balance = account_info['amount'] / 1_000_000
        
        print(f"\n💰 Contract Balance:")
        print(f"   APP_ID: {app_id}")
        print(f"   Address: {app_addr}")
        print(f"   ALGO Balance: {balance} ALGO")
        
        # Try to get app info
        try:
            app_info = algod_client.application_info(app_id)
            print(f"   Status: Active")
        except:
            print(f"   Status: Unknown")
        
        print(f"   Explorer: https://testnet.algoexplorer.io/address/{app_addr}")
        print(f"   App Explorer: https://testnet.algoexplorer.io/application/{app_id}")
        
    except Exception as e:
        print(f"❌ Could not check contract balance: {e}")

def check_deployment_balances():
    """Check balances of all deployed contracts"""
    print("📊 Check All Deployment Balances")
    
    # Check for deployment files
    deployment_files = [
        ("Simple Contract", "simple_deployment.json"),
        ("Advanced Vault", "advanced_vault_deployment.json"),
        ("Sender Contract", "sender_contract_deployment.json"),
        ("OGC Token", "ogc_token_info.json")
    ]
    
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    found_any = False
    
    for name, filename in deployment_files:
        if os.path.exists(filename):
            found_any = True
            try:
                with open(filename, 'r') as f:
                    info = json.load(f)
                
                if 'appId' in info:
                    # It's a contract
                    app_addr = logic.get_application_address(info['appId'])
                    account_info = algod_client.account_info(app_addr)
                    balance = account_info['amount'] / 1_000_000
                    
                    print(f"\n🏦 {name}:")
                    print(f"   APP_ID: {info['appId']}")
                    print(f"   Balance: {balance} ALGO")
                    
                elif 'assetId' in info:
                    # It's a token
                    print(f"\n🪙 {name}:")
                    print(f"   Asset ID: {info['assetId']}")
                    print(f"   Creator: {info['creator']}")
                    
            except Exception as e:
                print(f"\n❌ {name}: Could not check - {e}")
    
    if not found_any:
        print("❌ No deployment files found")
        print("Deploy contracts first to see their balances")

def check_all_wallets():
    """Check balances of all wallets"""
    print("👥 Check All Wallet Balances")
    
    wallets = load_wallets()
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
    
    for name, wallet_info in wallets.items():
        try:
            account_info = algod_client.account_info(wallet_info['addr'])
            balance = account_info['amount'] / 1_000_000
            
            print(f"\n💳 {name}:")
            print(f"   Address: {wallet_info['addr']}")
            print(f"   Balance: {balance} ALGO")
            
        except Exception as e:
            print(f"\n❌ {name}: Could not check - {e}")

def main():
    """Main balance checking menu"""
    while True:
        print("\n💰 Balance Checker")
        print("1. Check wallet balance (from selector)")
        print("2. Check any address balance")
        print("3. Check contract balance (APP_ID)")
        print("4. Check all deployments")
        print("5. Check all wallets")
        print("6. Exit")
        
        choice = input("Choose (1-6): ").strip()
        
        if choice == "1":
            check_wallet_balance()
        elif choice == "2":
            check_address_balance()
        elif choice == "3":
            check_contract_balance()
        elif choice == "4":
            check_deployment_balances()
        elif choice == "5":
            check_all_wallets()
        elif choice == "6":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()