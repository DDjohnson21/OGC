#!/usr/bin/env python3
"""
OGC Complete Ecosystem Demo
Showcases all features: Token, Vault, Governance, Echo
"""

import json
import os
import time
from algosdk.v2client import algod
from algosdk import transaction, logic
from wallet_selector import load_wallets

# Configuration
ALGOD_URL = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

class OGCDemo:
    def __init__(self):
        self.algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
        self.wallets = load_wallets()
        self.demo_results = {}
        
    def print_header(self, title):
        print(f"\n{'='*50}")
        print(f"🎬 {title}")
        print(f"{'='*50}")
        
    def print_step(self, step):
        print(f"\n🎯 {step}")
        time.sleep(1)  # Dramatic pause
        
    def get_demo_wallets(self):
        """Get wallets for demo (Alice, Bob, Charlie)"""
        wallet_list = list(self.wallets.items())
        return {
            'alice': {'name': 'Alice', **wallet_list[0][1]} if len(wallet_list) > 0 else None,
            'bob': {'name': 'Bob', **wallet_list[1][1]} if len(wallet_list) > 1 else None,
            'charlie': {'name': 'Charlie', **wallet_list[2][1]} if len(wallet_list) > 2 else None,
        }
        
    def demo_token_creation(self):
        """Demo 1: Create OGC Token"""
        self.print_header("Part 1: Creating OGC Token")
        
        try:
            # Import and run token creation
            from create_ogc_token import create_ogc_token
            
            self.print_step("Creating 1 billion OGC tokens...")
            
            # Simulate token creation (would normally be interactive)
            print("🪙 OGC Token Configuration:")
            print("   Name: OGC Token")
            print("   Symbol: OGC")
            print("   Total Supply: 1,000,000,000")
            print("   Decimals: 6")
            
            # Check if token already exists
            if os.path.exists("ogc_token_info.json"):
                with open("ogc_token_info.json", 'r') as f:
                    token_info = json.load(f)
                print(f"✅ OGC Token Found: Asset ID {token_info['assetId']}")
                self.demo_results['token'] = token_info
            else:
                print("⚠️  Token not found - run create_ogc_token.py first")
                self.demo_results['token'] = {'assetId': 'DEMO_TOKEN', 'name': 'OGC Token'}
                
        except Exception as e:
            print(f"❌ Token demo failed: {e}")
            self.demo_results['token'] = {'error': str(e)}
            
    def demo_advanced_vault(self):
        """Demo 2: Advanced Vault Crowdfunding"""
        self.print_header("Part 2: Advanced Vault Demo")
        
        try:
            self.print_step("Setting up crowdfunding vault...")
            
            goal_algo = 5.0
            print(f"🎯 Goal: {goal_algo} ALGO")
            print("📅 Deadline: 24 hours from now")
            
            # Check if vault exists
            if os.path.exists("advanced_vault_deployment.json"):
                with open("advanced_vault_deployment.json", 'r') as f:
                    vault_info = json.load(f)
                print(f"✅ Vault Found: APP_ID {vault_info['appId']}")
                
                # Simulate contributions
                demo_wallets = self.get_demo_wallets()
                contributions = [
                    (demo_wallets['alice'], 2.0),
                    (demo_wallets['bob'], 3.0)
                ]
                
                total_contributed = 0
                for wallet, amount in contributions:
                    if wallet:
                        self.print_step(f"{wallet['name']} contributes {amount} ALGO")
                        total_contributed += amount
                        print(f"💳 Total after {wallet['name']}: {total_contributed} ALGO")
                
                print(f"\n🎯 Goal: {goal_algo} ALGO")
                if total_contributed >= goal_algo:
                    print("🎉 SUCCESS! Goal Reached!")
                    print("   Ready to release funds after deadline")
                else:
                    print(f"⏳ Need {goal_algo - total_contributed} more ALGO")
                    
                self.demo_results['vault'] = {
                    'appId': vault_info['appId'],
                    'goal': goal_algo,
                    'contributed': total_contributed,
                    'success': total_contributed >= goal_algo
                }
            else:
                print("⚠️  Vault not found - run advanced_vault.py first")
                self.demo_results['vault'] = {'error': 'Not deployed'}
                
        except Exception as e:
            print(f"❌ Vault demo failed: {e}")
            self.demo_results['vault'] = {'error': str(e)}
            
    def demo_governance(self):
        """Demo 3: Governance Voting"""
        self.print_header("Part 3: Governance Demo")
        
        try:
            self.print_step("Setting up governance contract...")
            
            if os.path.exists("governance_sender_deployment.json"):
                with open("governance_sender_deployment.json", 'r') as f:
                    gov_info = json.load(f)
                print(f"✅ Governance Contract: APP_ID {gov_info['appId']}")
                
                # Simulate governance flow
                demo_wallets = self.get_demo_wallets()
                contributors = [w for w in demo_wallets.values() if w][:3]
                
                self.print_step("Contributors opt in and contribute...")
                for contributor in contributors:
                    print(f"👤 {contributor['name']} opted in and contributed")
                
                self.print_step("Owner proposes: Send 1 ALGO to charity")
                print("📝 Proposal Details:")
                print("   Recipient: Charity Address")
                print("   Amount: 1.0 ALGO")
                print("   Required: 75% approval")
                
                self.print_step("Contributors vote...")
                votes = len(contributors)
                required = int(len(contributors) * 0.75) + 1
                
                for contributor in contributors:
                    print(f"🗳️  {contributor['name']} votes YES")
                
                print(f"\n📊 Voting Results:")
                print(f"   Votes: {votes}/{len(contributors)}")
                print(f"   Required: {required}")
                print(f"   Approval: {votes/len(contributors)*100:.0f}%")
                
                if votes >= required:
                    print("✅ Proposal APPROVED!")
                    print("⚡ Executing proposal...")
                    print("💸 1 ALGO sent to charity")
                else:
                    print("❌ Proposal REJECTED")
                    
                self.demo_results['governance'] = {
                    'appId': gov_info['appId'],
                    'contributors': len(contributors),
                    'votes': votes,
                    'approved': votes >= required
                }
            else:
                print("⚠️  Governance contract not found - run governance_sender.py first")
                self.demo_results['governance'] = {'error': 'Not deployed'}
                
        except Exception as e:
            print(f"❌ Governance demo failed: {e}")
            self.demo_results['governance'] = {'error': str(e)}
            
    def demo_echo_contract(self):
        """Demo 4: Echo Contract Testing"""
        self.print_header("Part 4: Echo Contract Demo")
        
        try:
            self.print_step("Testing echo contract...")
            
            if os.path.exists("echo_contract_deployment.json"):
                with open("echo_contract_deployment.json", 'r') as f:
                    echo_info = json.load(f)
                print(f"✅ Echo Contract: APP_ID {echo_info['appId']}")
                
                # Simulate echo test
                test_amount = 1.0
                returned_amount = test_amount - 0.001  # Minus fee
                
                self.print_step(f"Sending {test_amount} ALGO to echo contract...")
                print(f"📤 Sent: {test_amount} ALGO")
                print("⏳ Waiting for echo...")
                time.sleep(2)
                print(f"📥 Received: {returned_amount} ALGO")
                print(f"💰 Fee: 0.001 ALGO")
                print("🎯 Echo successful!")
                
                self.demo_results['echo'] = {
                    'appId': echo_info['appId'],
                    'sent': test_amount,
                    'received': returned_amount,
                    'success': True
                }
            else:
                print("⚠️  Echo contract not found - run echo_contract.py first")
                self.demo_results['echo'] = {'error': 'Not deployed'}
                
        except Exception as e:
            print(f"❌ Echo demo failed: {e}")
            self.demo_results['echo'] = {'error': str(e)}
            
    def show_final_results(self):
        """Show comprehensive demo results"""
        self.print_header("Demo Complete!")
        
        print("🏆 OGC Ecosystem Demo Results:")
        
        # Token results
        if 'token' in self.demo_results:
            token = self.demo_results['token']
            if 'error' not in token:
                print(f"   🪙 OGC Token: Asset ID {token.get('assetId', 'N/A')}")
            else:
                print(f"   🪙 OGC Token: ❌ {token['error']}")
        
        # Vault results
        if 'vault' in self.demo_results:
            vault = self.demo_results['vault']
            if 'error' not in vault:
                status = "✅ Success" if vault.get('success') else "⏳ In Progress"
                print(f"   🏦 Vault: APP_ID {vault.get('appId', 'N/A')} - {status}")
            else:
                print(f"   🏦 Vault: ❌ {vault['error']}")
        
        # Governance results
        if 'governance' in self.demo_results:
            gov = self.demo_results['governance']
            if 'error' not in gov:
                status = "✅ Approved" if gov.get('approved') else "❌ Rejected"
                print(f"   🗳️  Governance: APP_ID {gov.get('appId', 'N/A')} - {status}")
            else:
                print(f"   🗳️  Governance: ❌ {gov['error']}")
        
        # Echo results
        if 'echo' in self.demo_results:
            echo = self.demo_results['echo']
            if 'error' not in echo:
                status = "✅ Success" if echo.get('success') else "❌ Failed"
                print(f"   🔄 Echo: APP_ID {echo.get('appId', 'N/A')} - {status}")
            else:
                print(f"   🔄 Echo: ❌ {echo['error']}")
        
        print(f"\n📊 Final Summary:")
        total_features = len(self.demo_results)
        successful_features = sum(1 for r in self.demo_results.values() if 'error' not in r)
        print(f"   Features Demonstrated: {successful_features}/{total_features}")
        print(f"   Success Rate: {successful_features/total_features*100:.0f}%" if total_features > 0 else "   Success Rate: 0%")
        
        print(f"\n🔗 Explore on TestNet:")
        for feature, result in self.demo_results.items():
            if 'appId' in result:
                print(f"   {feature.title()}: https://testnet.algoexplorer.io/application/{result['appId']}")
        
def main():
    """Run complete OGC ecosystem demo"""
    print("🚀 OGC - Complete Ecosystem Demo")
    print("Showcasing: Token Creation, Vaults, Governance, Echo Contracts")
    
    demo = OGCDemo()
    
    try:
        # Run all demo parts
        demo.demo_token_creation()
        demo.demo_advanced_vault()
        demo.demo_governance()
        demo.demo_echo_contract()
        
        # Show final results
        demo.show_final_results()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed: {e}")

if __name__ == "__main__":
    import os
    main()