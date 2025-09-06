# OGC - Out The Groupchat

## ALGO Storage Smart Contract

This project contains a functional ALGO token storage smart contract built for the Algorand blockchain using PyTeal. It's perfect for beginners who want to learn how to create and deploy real smart contracts that handle cryptocurrency on Algorand.

## 🚀 What This Contract Does

The smart contract stores and manages ALGO tokens (Algorand's native cryptocurrency) on the blockchain. It demonstrates:

- Creating a smart contract using PyTeal
- Storing and managing ALGO tokens
- User balance tracking and management
- Deposit and withdrawal functionality
- Global and local state management
- User opt-in/opt-out functionality
- Deploying to Algorand testnet

## 📁 Project Structure

```
OGC/
├── hello_world_contract.py    # PyTeal source code (ALGO storage contract)
├── approval.teal             # Compiled approval program
├── clear.teal               # Compiled clear program
├── deploy_contract.js        # Basic deployment script
├── deploy_with_account.js    # Complete deployment with account creation
├── deploy_algo_contract.js   # ALGO contract deployment script
├── simple_test.js           # Simple contract testing script
├── test_contract.js         # Contract testing script
├── deployment_info.json      # Deployment information
├── package.json             # Node.js dependencies
├── venv/                    # Python virtual environment
└── README.md               # This file
```

## 🛠️ Prerequisites

- Node.js (v14 or higher)
- Python 3.7 or higher
- An Algorand testnet account with some ALGO tokens

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Activate Python virtual environment
source venv/bin/activate

# Install Python dependencies (already done)
pip install pyteal
```

### 2. Compile the Contract

```bash
# Compile the ALGO storage contract
npm run compile
```

This will generate:

- `approval.teal` - The main contract logic
- `clear.teal` - Contract cleanup logic

### 3. Test the Contract

```bash
# Test the compiled contract
npm run test-algo
```

This will:

- Verify the contract compiles correctly
- Show contract features and actions
- Create a test account
- Display next steps

### 4. Deploy to Testnet

#### Option A: Simple Testing

```bash
# Run everything at once (compile + test)
npm start
```

#### Option B: Manual Deployment

```bash
# Deploy the ALGO contract
npm run deploy-algo
```

This will:

- Create a new testnet account
- Guide you through funding it
- Deploy the contract automatically
- Test deposit/withdraw functionality

## 🔧 Contract Details

### Smart Contract Features

The contract is written in PyTeal and provides:

1. **ALGO Token Storage**: Stores and manages Algorand's native ALGO tokens
2. **User Balance Tracking**: Tracks individual user balances in local state
3. **Global State Management**: Tracks total deposits and user count
4. **Deposit/Withdraw**: Users can deposit and withdraw ALGO tokens
5. **User Management**: Users must opt-in to use the contract
6. **Transaction Logging**: All operations are logged for transparency

### Contract Actions

- **Action 0**: Deposit ALGO tokens
- **Action 1**: Withdraw ALGO tokens
- **Action 2**: Get user balance
- **Action 3**: Get contract information

### State Management

**Global State:**

- `total_deposited`: Total ALGO deposited by all users
- `total_users`: Number of users who opted in
- `contract_active`: Contract status flag

**Local State (per user):**

- `user_balance`: User's current ALGO balance
- `user_deposits`: User's total deposits

## 📊 Contract Information

- **Program Version**: 5
- **Approval Program**: 188 lines of TEAL
- **Clear Program**: 3 lines of TEAL
- **Global State**: 3 integer values
- **Local State**: 2 integer values per user

## 🧪 Testing the Contract

After deployment, you can:

1. **View on AlgoExplorer**: Check your contract on [AlgoExplorer Testnet](https://testnet.algoexplorer.io)
2. **Check Logs**: The contract logs all operations (deposits, withdrawals, balances)
3. **Verify State**: Confirm ALGO balances are stored in local and global state
4. **Test Functions**: Use the contract actions to deposit, withdraw, and check balances

## 🚀 How to Run Everything

### Quick Start (Recommended)

```bash
# 1. Install dependencies
npm install

# 2. Run everything at once
npm start
```

This will:

- Compile the contract
- Test the contract
- Show you how to deploy

### Step-by-Step Instructions

```bash
# 1. Install dependencies
npm install

# 2. Compile the contract
npm run compile

# 3. Test the contract
npm run test-algo

# 4. Deploy to testnet (optional)
npm run deploy-algo
```

### Available Commands

| Command               | Description                     |
| --------------------- | ------------------------------- |
| `npm run compile`     | Compile PyTeal contract to TEAL |
| `npm run test-algo`   | Test the compiled contract      |
| `npm run deploy-algo` | Deploy contract to testnet      |
| `npm start`           | Run compile + test              |
| `npm run deploy`      | Basic deployment script         |
| `npm run test`        | Test deployed contract          |

### Manual Steps

If you want to run things manually:

```bash
# 1. Activate Python environment
source venv/bin/activate

# 2. Compile contract
python3 hello_world_contract.py

# 3. Test contract
node simple_test.js

# 4. Deploy contract
node deploy_algo_contract.js
```

## 🔗 Useful Links

- [Algorand Testnet Dispenser](https://testnet.algoexplorer.io/dispenser) - Get free testnet ALGO
- [AlgoExplorer Testnet](https://testnet.algoexplorer.io) - View your transactions
- [PyTeal Documentation](https://pyteal.readthedocs.io/) - Learn more about PyTeal
- [Algorand Developer Portal](https://developer.algorand.org/) - Official Algorand docs

## 🎓 Learning Resources

This project is designed for beginners. Here's what you can learn:

1. **PyTeal Basics**: How to write smart contracts in Python
2. **Algorand Concepts**: Global state, local state, applications, transactions
3. **Token Management**: How to handle ALGO tokens in smart contracts
4. **User Management**: Opt-in/opt-out functionality
5. **State Management**: Global vs local state usage
6. **Deployment Process**: How to deploy contracts to testnet
7. **SDK Usage**: Using the Algorand JavaScript SDK

## 🚨 Important Notes

- **Testnet Only**: This contract is for testnet only
- **Save Your Mnemonic**: Always save your account mnemonic phrase
- **Free Tokens**: Testnet ALGO is free from the dispenser
- **No Real Value**: Testnet tokens have no real value
- **User Opt-in Required**: Users must opt-in to use the contract

## 🔄 Next Steps

Once you understand this contract, you can:

1. Add more token types (ASAs)
2. Implement interest calculations
3. Add user authentication
4. Create a frontend interface
5. Add more complex business logic
6. Deploy to mainnet (with real ALGO)
7. Create a token exchange
8. Build a DeFi application

## 🤝 Contributing

Feel free to fork this project and experiment! This is a learning project, so:

- Try modifying the contract logic
- Add new features
- Create better deployment scripts
- Share your improvements

## 📝 License

This project is open source and available under the MIT License.

---

**Happy coding on Algorand! 🚀**
