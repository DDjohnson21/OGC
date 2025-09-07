# OGC Tangible Demo Commands

## 📍 Where to Run Commands

**All commands must be run from:**
```bash
/Users/eltonbaidoo/OGC/ogc-contracts/projects/ogc-contracts/
```

## 🚀 Quick Start

### 1. Navigate & Activate
```bash
cd ~/OGC/ogc-contracts/projects/ogc-contracts
source "$(poetry env info --path)/bin/activate"
python --version  # Should show 3.13.x
```

### 2. Create OGC Token
```bash
python create_ogc_token.py
```
**Expected Output:**
```
🪙 Creating OGC Token...
✅ OGC Token Created!
   Asset ID: 1033
   Total Supply: 1,000,000,000 OGC
   Creator: VYXZFE4BGH...
```

### 3. Verify Token
```bash
python verify_token.py
```
**Expected Output:**
```
🔍 Verifying OGC Token...
✅ OGC Token Found!
   Asset ID: 1033
   Name: OGC Token
   Unit: OGC
   Total: 1,000,000,000
```

### 4. Demo ALGO Vault
```bash
python ogc_demo.py
```
**Expected Output:**
```
🚀 OGC - Out The Groupchat Demo
🎯 Goal: 2.0 ALGO
✅ Fund Created: APP_ID 1036
💰 Total: 1.5 ALGO
⏳ Need 0.5 more ALGO
```

### 5. Run Tests
```bash
python test_vault.py
```
**Expected Output:**
```
🧪 Testing OGC Vault Basic Flow
✅ Deployed: APP_ID 1037
✅ Contribution test passed: 0.5 ALGO
🏁 Tests PASSED
```

## 🎯 One-Liner Commands

### Full Demo Sequence
```bash
cd ~/OGC/ogc-contracts/projects/ogc-contracts && source "$(poetry env info --path)/bin/activate" && python create_ogc_token.py && python verify_token.py && python ogc_demo.py
```

### Quick Token Demo
```bash
python create_ogc_token.py && python verify_token.py
```

### Quick Vault Demo
```bash
python ogc_demo.py && python test_vault.py
```

## 🛠️ Makefile Commands

```bash
make demo    # Run ogc_demo.py
make test    # Run test_vault.py  
make build   # Build working_vault.py
make ci      # Run full pipeline
```

## 📊 What Each Command Does

| Command | Purpose | Output |
|---------|---------|---------|
| `create_ogc_token.py` | Mints OGC token on LocalNet | Asset ID number |
| `verify_token.py` | Confirms token exists | Token details |
| `ogc_demo.py` | Shows group funding scenario | ALGO vault demo |
| `test_vault.py` | Tests contract functions | Test results |
| `working_vault.py` | Builds smart contract | Artifacts created |

## 🎤 For Hackathon Presentation

**Run in this order:**
1. `python create_ogc_token.py` - "We minted OGC token"
2. `python verify_token.py` - "Token verified on Algorand"  
3. `python ogc_demo.py` - "Group funding demo"
4. `python test_vault.py` - "All tests pass"

## 🔧 Troubleshooting

**If commands fail:**
```bash
# Check you're in right directory
pwd  # Should show: /Users/eltonbaidoo/OGC/ogc-contracts/projects/ogc-contracts

# Check environment is active
which python  # Should show venv path

# Reactivate if needed
source "$(poetry env info --path)/bin/activate"
```