# 🚀 OGC - Out The Groupchat

**Complete Algorand Smart Contract Ecosystem**

A comprehensive DeFi platform featuring tokens, vaults, governance, and automated contracts on Algorand TestNet.

## ✨ **Features**

- 🪙 **OGC Token** - Custom ASA with 1B supply
- 🏦 **Advanced Vault** - Goal-based crowdfunding with deadlines
- 📤 **Sender Contract** - Send ALGO from contract to any wallet
- 🔄 **Echo Contract** - Risk-free testing (auto bounce-back)
- 💳 **Multi-Wallet Support** - 3 TestNet wallets configured
- 🎭 **Interactive Demos** - Choose-your-own-adventure testing

## 🚀 **Quick Start**

### **1. Environment Setup**

```bash
# Navigate to project
cd ~/OGC

# Activate virtual environment
source ogc-contracts/projects/ogc-contracts/venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt
```

### **2. Fund TestNet Wallets**

```bash
# Check wallet balances
python check_any_balance.py
# Choose option 5: Check all wallets

# Get TestNet ALGO from dispenser:
# https://testnet.algoexplorer.io/dispenser
# Fund these addresses with 5+ ALGO each:
# - 63W3II7K5X2OYPMX4DSMNOK4HY33UFJRI2MQ2OFDUHF47LFLUNIUJTDN4U
# - SXIEIE2D7FOKUNQXUFUZIRYKE75RYD5KBN5BOYZFXLIL7LOTFX4VK3U7CE
# - TR5YH6EHNKNE24OSMCOXK7B4DKL6DYBGIZAYZUORAOL2C5ILR2ASVOYAPQ
```

### **3. Interactive Demo**

```bash
# Run interactive demo
python ogc_demo.py
# Choose option 5: Full Ecosystem Demo
```

## 🧪 **Testing Commands**

### **Deploy All Contracts**

```bash
python create_ogc_token.py          # Create OGC token
python advanced_vault.py            # Deploy vault (goal: 2 ALGO, 24 hours)
python sender_contract.py           # Deploy sender (fund with 5 ALGO)
python echo_contract.py             # Deploy echo (fund with 3 ALGO)
```

### **Test Individual Features**

```bash
# Token testing
python token_interact.py            # Opt-in, transfer tokens

# Vault testing  
python vault_interact.py            # Contribute, check status, release

# Sender testing
python sender_interact.py           # Send ALGO from contract

# Echo testing
python echo_interact.py             # Test bounce-back (send 1 ALGO, get 0.999 back)

# Simple contract testing
python simple_deploy_multi.py       # Deploy simple
python simple_deposit.py optin      # Opt-in
python simple_deposit.py deposit 2  # Trigger refund
```

### **Status & Balance Checks**

```bash
python check_any_balance.py         # Check all balances
python ogc_demo.py                  # Choose option 7: Deployment status
python full_demo.py                 # Automated demo of all features
```

## 📁 **Project Structure**

```
OGC/
├── README.md                       # This file
├── TESTING_GUIDE.md               # Comprehensive testing docs
├── wallets.json                   # TestNet wallet configurations
├── create_ogc_token.py            # OGC token creation
├── advanced_vault.py              # Crowdfunding vault
├── sender_contract.py             # ALGO sender contract
├── echo_contract.py               # Auto bounce-back contract
├── ogc_demo.py                    # Interactive demo
├── full_demo.py                   # Automated ecosystem demo
├── check_any_balance.py           # Balance utilities
└── *_interact.py                  # Contract interaction scripts
```

## 🎯 **Smart Contracts**

### **OGC Token (ASA)**
- **Supply**: 1,000,000,000 OGC
- **Decimals**: 6
- **Features**: Standard Algorand asset with opt-in required

### **Advanced Vault**
- **Purpose**: Goal-based crowdfunding
- **Features**: Deadline enforcement, automatic release
- **Usage**: Set goal + deadline, contributors fund, auto-release when conditions met

### **Sender Contract**
- **Purpose**: Send ALGO from contract to any wallet
- **Features**: Owner-controlled, tracks total sent
- **Usage**: Fund contract, then send to any address

### **Echo Contract**
- **Purpose**: Risk-free testing and demos
- **Features**: Automatically bounces ALGO back (minus 0.001 fee)
- **Usage**: Send ALGO, get it back immediately

### **Simple Contract**
- **Purpose**: Basic deposit/refund mechanism
- **Features**: Auto-refund at 2 ALGO threshold
- **Usage**: Opt-in, deposit, automatic refund

## 🛠 **Technical Stack**

- **Blockchain**: Algorand TestNet
- **SDK**: py-algorand-sdk 2.6.0
- **Smart Contracts**: PyTeal/TEAL
- **Language**: Python 3.7+
- **Network**: TestNet via Algonode API

## 🎬 **Demo Scenarios**

### **Scenario 1: Complete Ecosystem**
```bash
python full_demo.py
# Showcases all features in sequence
```

### **Scenario 2: Individual Testing**
```bash
python ogc_demo.py
# Choose specific features to test
```

### **Scenario 3: Custom Demo**
```bash
python ogc_demo.py
# Choose option 6: Custom Demo
# Select multiple features: 1,2,4
```

## 🔗 **TestNet Links**

- **Dispenser**: https://testnet.algoexplorer.io/dispenser
- **Explorer**: https://testnet.algoexplorer.io/
- **API**: https://testnet-api.algonode.cloud

## 📊 **Success Indicators**

When everything works correctly:
- ✅ All contracts deploy successfully
- ✅ Tokens transfer between wallets
- ✅ Vault accepts contributions and releases funds
- ✅ Echo contract bounces ALGO back
- ✅ Sender contract sends to any address
- ✅ Demo shows "Success Rate: 100%"

## 🚨 **Troubleshooting**

### **Common Issues**
- **"Insufficient Balance"**: Fund wallets with TestNet ALGO
- **"Contract Not Found"**: Deploy contracts first
- **"Opt-in Required"**: Run opt-in commands before interactions

### **Quick Fixes**
```bash
# Check what's deployed
python ogc_demo.py → option 7

# Check wallet balances
python check_any_balance.py → option 5

# Get help
python ogc_demo.py → follow menu options
```

## 🎯 **Getting Started**

1. **Setup environment** (activate venv, install deps)
2. **Fund wallets** (get TestNet ALGO)
3. **Run demo** (`python ogc_demo.py`)
4. **Deploy contracts** (follow prompts)
5. **Test features** (use interaction scripts)

**Ready to explore the OGC ecosystem!** 🚀✨

---

**Built for Algorand Hackathon - Complete DeFi ecosystem on TestNet**