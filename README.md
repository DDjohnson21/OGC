# 🐍 Python Algorand Smart Contract System

Your complete Algorand smart contract system has been successfully converted to Python!

## 🚀 **Quick Start**

### **1. Setup**

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Deploy Contract**

```bash
python simple_deploy.py
```

### **3. Use Contract**

```bash
# Opt into the contract
python simple_deposit.py optin

# Make deposits to get money back
python simple_deposit.py deposit 2

# Check contract info
python simple_deposit.py info
```

### **4. Manage Wallet**

```bash
# Check balance
python simple_wallet.py balance

# Send ALGO
python simple_wallet.py send <address> <amount>

# Get funding instructions
python simple_wallet.py fund
```

## 📁 **Python Files**

| File                | Purpose                   | Example Usage                        |
| ------------------- | ------------------------- | ------------------------------------ |
| `simple_deploy.py`  | Deploy smart contracts    | `python simple_deploy.py`            |
| `simple_deposit.py` | Interact with contracts   | `python simple_deposit.py deposit 2` |
| `simple_wallet.py`  | Manage wallet & send ALGO | `python simple_wallet.py balance`    |
| `setup.py`          | Setup environment         | `python setup.py`                    |
| `requirements.txt`  | Python dependencies       | `pip install -r requirements.txt`    |

## 🎯 **How the Smart Contract Works**

1. **Deposit ALGO**: Send 1+ ALGO to the contract
2. **Threshold**: When you reach 2 ALGO total deposits
3. **Auto-Refund**: Contract automatically sends 2 ALGO back
4. **Success Log**: Contract logs "success" when refund happens

## 🔄 **Complete Workflow Example**

```bash
# 1. Setup environment
source venv/bin/activate

# 2. Deploy contract (if not already deployed)
python simple_deploy.py

# 3. Opt into contract
python simple_deposit.py optin

# 4. Make deposit to trigger refund
python simple_deposit.py deposit 2
# Expected output: App Logs: ['success']

# 5. Check your balance (should have received 2 ALGO back)
python simple_wallet.py balance
```

## 💡 **Key Features**

✅ **Same functionality as JavaScript version**  
✅ **Compatible with existing wallet & deployment files**  
✅ **Uses py-algorand-sdk 2.6.0**  
✅ **Clean error handling**  
✅ **Virtual environment setup**

## 🛠 **Dependencies**

- **Python 3.7+**
- **py-algorand-sdk 2.6.0**
- **Virtual environment (recommended)**

## 📊 **Commands Summary**

### **Deployment**

- `python simple_deploy.py` - Deploy smart contract

### **Contract Interaction**

- `python simple_deposit.py optin` - Opt into contract
- `python simple_deposit.py deposit <amount>` - Make deposit
- `python simple_deposit.py info` - Get contract info

### **Wallet Management**

- `python simple_wallet.py balance` - Check balance
- `python simple_wallet.py send <address> <amount>` - Send ALGO
- `python simple_wallet.py fund` - Get funding instructions

## 🎉 **Success Indicators**

When your smart contract works correctly, you'll see:

```bash
python simple_deposit.py deposit 2
```

**Expected Output:**

```
Sent grouped deposit txs. Group ID (first tx): [TX_ID]
App Logs: ['success']
```

This means the contract automatically sent 2 ALGO back to your wallet! 🚀

---

**Your Algorand smart contract system is now fully operational in Python!** 🐍✨
