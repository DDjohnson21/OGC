#!/usr/bin/env python3
"""
OGC Interactive Demo
Choose your own adventure through OGC features
"""

import json
import os
import time
from algosdk.v2client import algod
from wallet_selector import load_wallets

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

class InteractiveDemo:
    def __init__(self):
        self.algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
        self.wallets = load_wallets()
        
    def print_banner(self):
        print("""
🎭 OGC Interactive Demo
═══════════════════════════════════════════════════════════
   Explore the Out The Groupchat ecosystem
   Choose your own adventure through our features!
═══════════════════════════════════════════════════════════
        """)
        
    def show_main_menu(self):
        print("\n🎯 Choose Your Demo Adventure:")
        print("1. 🪙 Token Demo (Create & Transfer OGC)")
        print("2. 🏦 Vault Demo (Crowdfunding simulation)")
        print("3. 🗳️  Governance Demo (Democratic decisions)")
        print("4. 🔄 Echo Demo (Risk-free testing)")
        print("5. 📊 Full Ecosystem Demo (All features)")
        print("6. 🎯 Custom Demo (Pick components)")
        print("7. 📋 Check Deployment Status")
        print("8. 🚪 Exit")
        
    def token_demo(self):
        """Interactive token demonstration"""
        print("\n🪙 OGC Token Demo")
        print("═" * 30)
        
        if os.path.exists("ogc_token_info.json"):
            with open("ogc_token_info.json", 'r') as f:
                token_info = json.load(f)
            
            print(f"✅ OGC Token Found!")
            print(f"   Asset ID: {token_info['assetId']}")
            print(f"   Name: {token_info['name']}")
            print(f"   Total Supply: {token_info['total']:,} {token_info['unitName']}")
            print(f"   Creator: {token_info['creator']}")
            
            print(f"\n🔗 View on Explorer:")
            print(f"   https://testnet.algoexplorer.io/asset/{token_info['assetId']}")
            
            # Offer token interactions
            print(f"\n💡 What you can do:")
            print(f"   • Run: python token_interact.py")
            print(f"   • Opt into token")
            print(f"   • Transfer tokens between wallets")
            print(f"   • Check token balances")
            
        else:
            print("❌ OGC Token not found")
            print("💡 Create it first:")
            print("   python create_ogc_token.py")
            
    def vault_demo(self):
        """Interactive vault demonstration"""
        print("\n🏦 Advanced Vault Demo")
        print("═" * 30)
        
        if os.path.exists("advanced_vault_deployment.json"):
            with open("advanced_vault_deployment.json", 'r') as f:
                vault_info = json.load(f)
            
            print(f"✅ Advanced Vault Found!")
            print(f"   APP_ID: {vault_info['appId']}")
            print(f"   Goal: {vault_info['goal']/1_000_000} ALGO")
            print(f"   Receiver: {vault_info['receiver']}")
            
            # Check current balance
            try:
                account_info = self.algod_client.account_info(vault_info['appAddress'])
                balance = account_info['amount'] / 1_000_000
                goal = vault_info['goal'] / 1_000_000
                progress = (balance / goal) * 100 if goal > 0 else 0
                
                print(f"\n📊 Current Status:")
                print(f"   Balance: {balance} ALGO")
                print(f"   Progress: {progress:.1f}%")
                print(f"   Status: {'✅ Goal Reached!' if balance >= goal else '⏳ In Progress'}")
                
            except Exception as e:
                print(f"   ❌ Could not check status: {e}")
            
            print(f"\n🔗 View on Explorer:")
            print(f"   https://testnet.algoexplorer.io/application/{vault_info['appId']}")
            
            print(f"\n💡 What you can do:")
            print(f"   • Run: python vault_interact.py")
            print(f"   • Contribute to vault")
            print(f"   • Release funds (after deadline)")
            print(f"   • Check vault status")
            
        else:
            print("❌ Advanced Vault not found")
            print("💡 Deploy it first:")
            print("   python advanced_vault.py")
            
    def governance_demo(self):
        """Interactive governance demonstration"""
        print("\n🗳️  Governance Demo")
        print("═" * 30)
        
        if os.path.exists("governance_sender_deployment.json"):
            with open("governance_sender_deployment.json", 'r') as f:
                gov_info = json.load(f)
            
            print(f"✅ Governance Contract Found!")
            print(f"   APP_ID: {gov_info['appId']}")
            print(f"   Owner: {gov_info['owner']}")
            print(f"   Governance: {gov_info['governance']}")
            
            print(f"\n🗳️  How Governance Works:")
            print(f"   1. Contributors opt in and contribute ALGO")
            print(f"   2. Owner proposes sending ALGO somewhere")
            print(f"   3. Contributors vote on proposals")
            print(f"   4. Need 75% approval to execute")
            print(f"   5. Anyone can execute approved proposals")
            
            print(f"\n🔗 View on Explorer:")
            print(f"   https://testnet.algoexplorer.io/application/{gov_info['appId']}")
            
            print(f"\n💡 What you can do:")
            print(f"   • Run: python governance_interact.py")
            print(f"   • Opt in as contributor")
            print(f"   • Contribute ALGO")
            print(f"   • Vote on proposals")
            print(f"   • Execute approved proposals")
            
        else:
            print("❌ Governance Contract not found")
            print("💡 Deploy it first:")
            print("   python governance_sender.py")
            
    def echo_demo(self):
        """Interactive echo demonstration"""
        print("\n🔄 Echo Contract Demo")
        print("═" * 30)
        
        if os.path.exists("echo_contract_deployment.json"):
            with open("echo_contract_deployment.json", 'r') as f:
                echo_info = json.load(f)
            
            print(f"✅ Echo Contract Found!")
            print(f"   APP_ID: {echo_info['appId']}")
            print(f"   Address: {echo_info['appAddress']}")
            
            # Check contract balance
            try:
                account_info = self.algod_client.account_info(echo_info['appAddress'])
                balance = account_info['amount'] / 1_000_000
                
                print(f"\n📊 Contract Status:")
                print(f"   Balance: {balance} ALGO")
                print(f"   Status: {'✅ Ready for testing' if balance > 0.1 else '⚠️ Needs funding'}")
                
            except Exception as e:
                print(f"   ❌ Could not check status: {e}")
            
            print(f"\n🔄 How Echo Works:")
            print(f"   1. Send ALGO to the contract")
            print(f"   2. Contract automatically sends it back")
            print(f"   3. You lose only ~0.002 ALGO in fees")
            print(f"   4. Perfect for risk-free testing!")
            
            print(f"\n🔗 View on Explorer:")
            print(f"   https://testnet.algoexplorer.io/application/{echo_info['appId']}")
            
            print(f"\n💡 What you can do:")
            print(f"   • Run: python echo_interact.py")
            print(f"   • Test echo functionality")
            print(f"   • Fund contract for operations")
            print(f"   • Check echo statistics")
            
        else:
            print("❌ Echo Contract not found")
            print("💡 Deploy it first:")
            print("   python echo_contract.py")
            
    def full_ecosystem_demo(self):
        """Run the full ecosystem demo"""
        print("\n📊 Running Full Ecosystem Demo...")
        print("This will showcase all OGC features in sequence.")
        
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            try:
                from full_demo import main as run_full_demo
                run_full_demo()
            except ImportError:
                print("❌ full_demo.py not found")
            except Exception as e:
                print(f"❌ Demo failed: {e}")
        else:
            print("Demo cancelled")
            
    def custom_demo(self):
        """Custom demo builder"""
        print("\n🎯 Custom Demo Builder")
        print("Select which features to demonstrate:")
        
        features = {
            '1': ('Token Creation', self.token_demo),
            '2': ('Advanced Vault', self.vault_demo),
            '3': ('Governance', self.governance_demo),
            '4': ('Echo Contract', self.echo_demo)
        }
        
        print("\nAvailable features:")
        for key, (name, _) in features.items():
            print(f"   {key}. {name}")
        
        selections = input("\nEnter feature numbers (e.g., 1,3,4): ").strip()
        
        try:
            selected = [s.strip() for s in selections.split(',')]
            for selection in selected:
                if selection in features:
                    name, demo_func = features[selection]
                    print(f"\n{'='*50}")
                    print(f"Running {name} Demo...")
                    demo_func()
                    time.sleep(2)
                else:
                    print(f"❌ Invalid selection: {selection}")
        except Exception as e:
            print(f"❌ Custom demo failed: {e}")
            
    def check_deployment_status(self):
        """Check status of all deployments"""
        print("\n📋 Deployment Status Check")
        print("═" * 40)
        
        deployments = [
            ("OGC Token", "ogc_token_info.json", "assetId"),
            ("Simple Contract", "simple_deployment.json", "appId"),
            ("Advanced Vault", "advanced_vault_deployment.json", "appId"),
            ("Sender Contract", "sender_contract_deployment.json", "appId"),
            ("Governance Contract", "governance_sender_deployment.json", "appId"),
            ("Echo Contract", "echo_contract_deployment.json", "appId")
        ]
        
        deployed_count = 0
        total_count = len(deployments)
        
        for name, filename, id_key in deployments:
            if os.path.exists(filename):
                try:
                    with open(filename, 'r') as f:
                        info = json.load(f)
                    
                    print(f"✅ {name}: {id_key.upper()} {info[id_key]}")
                    deployed_count += 1
                except Exception as e:
                    print(f"❌ {name}: Error reading file - {e}")
            else:
                print(f"❌ {name}: Not deployed")
        
        print(f"\n📊 Summary: {deployed_count}/{total_count} contracts deployed")
        
        if deployed_count < total_count:
            print(f"\n💡 To deploy missing contracts:")
            missing = [
                ("OGC Token", "python create_ogc_token.py"),
                ("Simple Contract", "python simple_deploy_multi.py"),
                ("Advanced Vault", "python advanced_vault.py"),
                ("Sender Contract", "python sender_contract.py"),
                ("Governance Contract", "python governance_sender.py"),
                ("Echo Contract", "python echo_contract.py")
            ]
            
            for i, (name, filename, _) in enumerate(deployments):
                if not os.path.exists(filename):
                    print(f"   {missing[i][1]}")
                    
    def run(self):
        """Main demo loop"""
        self.print_banner()
        
        while True:
            self.show_main_menu()
            
            try:
                choice = input("\nEnter your choice (1-8): ").strip()
                
                if choice == '1':
                    self.token_demo()
                elif choice == '2':
                    self.vault_demo()
                elif choice == '3':
                    self.governance_demo()
                elif choice == '4':
                    self.echo_demo()
                elif choice == '5':
                    self.full_ecosystem_demo()
                elif choice == '6':
                    self.custom_demo()
                elif choice == '7':
                    self.check_deployment_status()
                elif choice == '8':
                    print("\n👋 Thanks for exploring OGC!")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-8.")
                    
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")

def main():
    """Run interactive OGC demo"""
    demo = InteractiveDemo()
    demo.run()

if __name__ == "__main__":
    main()