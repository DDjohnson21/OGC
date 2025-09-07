# OGC Testing Guide

## 🧪 Complete Testing Documentation

### Quick Start Testing
```bash
# 1. Run interactive demo
python ogc_demo.py

# 2. Run full ecosystem demo
python full_demo.py

# 3. Check deployment status
python ogc_demo.py → option 7
```

## 📋 Pre-Testing Checklist

### Environment Setup
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] TestNet ALGO available in wallets
- [ ] All 3 wallets configured in `wallets.json`

### Wallet Status Check
```bash
python check_any_balance.py → option 5
# Verify all wallets have sufficient ALGO (>1 ALGO each)
```

## 🎯 Feature Testing Matrix

### 1. Token Testing
| Test Case | Command | Expected Result |
|-----------|---------|----------------|
| Create Token | `python create_ogc_token.py` | Asset ID generated |
| Opt Into Token | `python token_interact.py → 1` | Successful opt-in |
| Transfer Tokens | `python token_interact.py → 2` | Tokens transferred |
| Check Balance | `python token_interact.py → 3` | Balance displayed |

**Success Criteria:**
- ✅ Asset ID created on TestNet
- ✅ All wallets can opt-in
- ✅ Tokens transfer between wallets
- ✅ Balances update correctly

### 2. Vault Testing
| Test Case | Command | Expected Result |
|-----------|---------|----------------|
| Deploy Vault | `python advanced_vault.py` | APP_ID generated |
| Contribute | `python vault_interact.py → 1` | ALGO contributed |
| Check Status | `python vault_interact.py → 3` | Progress shown |
| Release Funds | `python vault_interact.py → 2` | Funds released |

**Success Criteria:**
- ✅ Vault accepts contributions
- ✅ Goal tracking works
- ✅ Deadline enforcement
- ✅ Automatic release after goal+deadline

### 3. Governance Testing
| Test Case | Command | Expected Result |
|-----------|---------|----------------|
| Deploy Contract | `python governance_sender.py` | APP_ID generated |
| Opt In Contributors | `python governance_interact.py → 1` | Contributors opted in |
| Contribute ALGO | `python governance_interact.py → 2` | ALGO contributed |
| Propose Send | `python governance_interact.py → 3` | Proposal created |
| Vote on Proposal | `python governance_interact.py → 4` | Votes recorded |
| Execute Proposal | `python governance_interact.py → 5` | ALGO sent (if 75% approval) |

**Success Criteria:**
- ✅ Only contributors can vote
- ✅ 75% approval required
- ✅ Proposals execute correctly
- ✅ One vote per contributor

### 4. Echo Testing
| Test Case | Command | Expected Result |
|-----------|---------|----------------|
| Deploy Echo | `python echo_contract.py` | APP_ID generated |
| Fund Contract | `python echo_interact.py → 3` | Contract funded |
| Test Echo | `python echo_interact.py → 1` | ALGO bounced back |
| Check Stats | `python echo_interact.py → 2` | Statistics shown |

**Success Criteria:**
- ✅ ALGO sent back automatically
- ✅ Only ~0.001 ALGO fee deducted
- ✅ Statistics tracked correctly
- ✅ Contract maintains balance

### 5. Simple Contract Testing
| Test Case | Command | Expected Result |
|-----------|---------|----------------|
| Deploy Contract | `python simple_deploy_multi.py` | APP_ID generated |
| Opt In | `python simple_deposit.py optin` | Opt-in successful |
| Deposit ALGO | `python simple_deposit.py deposit 2` | Auto-refund triggered |
| Check Balance | `python simple_wallet.py balance` | Balance updated |

**Success Criteria:**
- ✅ Contract deploys successfully
- ✅ Opt-in works
- ✅ 2 ALGO threshold triggers refund
- ✅ "success" logged in transaction

## 🔍 Testing Scenarios

### Scenario 1: New User Flow
```bash
# 1. Check wallet balances
python check_any_balance.py → 5

# 2. Deploy all contracts
python create_ogc_token.py
python advanced_vault.py
python governance_sender.py
python echo_contract.py

# 3. Run full demo
python full_demo.py

# 4. Verify all features work
python ogc_demo.py → 7
```

### Scenario 2: Individual Feature Testing
```bash
# Test specific feature
python ogc_demo.py
# Choose option 1-4 for individual tests
```

### Scenario 3: Integration Testing
```bash
# Test feature interactions
python ogc_demo.py → 6 (Custom Demo)
# Select multiple features: 1,2,3,4
```

## 🚨 Common Issues & Solutions

### Issue: "Insufficient Balance"
**Solution:**
```bash
# Get TestNet ALGO
# Visit: https://testnet.algoexplorer.io/dispenser
# Or check balance: python check_any_balance.py
```

### Issue: "Contract Not Found"
**Solution:**
```bash
# Check deployment status
python ogc_demo.py → 7
# Deploy missing contracts as shown
```

### Issue: "Opt-in Required"
**Solution:**
```bash
# For tokens: python token_interact.py → 1
# For governance: python governance_interact.py → 1
# For simple: python simple_deposit.py optin
```

### Issue: "75% Approval Not Met"
**Solution:**
```bash
# Need more contributors to vote
# Each contributor must: opt-in → contribute → vote
```

## 📊 Test Results Validation

### Successful Test Indicators
- ✅ **Green checkmarks** in demo outputs
- ✅ **Transaction IDs** generated
- ✅ **Explorer links** work
- ✅ **Balances update** correctly
- ✅ **No error messages**

### Failed Test Indicators
- ❌ **Red X marks** in outputs
- ❌ **Error messages** displayed
- ❌ **Transactions fail**
- ❌ **Balances don't update**

## 🔗 Verification Links

### TestNet Explorers
- **Transactions**: `https://testnet.algoexplorer.io/tx/[TX_ID]`
- **Applications**: `https://testnet.algoexplorer.io/application/[APP_ID]`
- **Assets**: `https://testnet.algoexplorer.io/asset/[ASSET_ID]`
- **Addresses**: `https://testnet.algoexplorer.io/address/[ADDRESS]`

### Quick Verification
```bash
# Check all deployments
python ogc_demo.py → 7

# Check all wallet balances  
python check_any_balance.py → 5

# Run comprehensive test
python full_demo.py
```

## 🎯 Testing Best Practices

### Before Testing
1. **Fund wallets** with TestNet ALGO
2. **Check deployment status**
3. **Verify environment setup**

### During Testing
1. **Read all output messages**
2. **Note transaction IDs**
3. **Verify on TestNet explorer**
4. **Test edge cases**

### After Testing
1. **Document results**
2. **Check final balances**
3. **Verify all features work**
4. **Clean up if needed**

## 📈 Success Metrics

### Complete Success
- All contracts deployed ✅
- All features functional ✅
- All tests pass ✅
- No errors encountered ✅

### Partial Success
- Most features work ✅
- Minor issues documented ⚠️
- Workarounds available 🔧

### Needs Work
- Multiple failures ❌
- Core features broken ❌
- Environment issues ❌

---

**Happy Testing! 🧪✨**