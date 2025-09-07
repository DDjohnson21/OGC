# OGC TestNet Demo Guide

## 🚀 Quick Demo Steps

### 1. Deploy Vault
```bash
python deploy_with_address.py
```
- Enter your 25-word mnemonic
- Note the APP_ID and APP_ADDRESS

### 2. Send ALGO via Pera
- Open Pera Wallet → TestNet
- Send 2+ ALGO to APP_ADDRESS
- Confirm transaction

### 3. Check Balance
```bash
python check_balance_testnet.py
# Enter APP_ID when prompted
```

### 4. Get App Address (if needed)
```bash
python get_app_address.py
# Enter APP_ID when prompted
```

### 5. Trigger Release (after goal met)
```bash
python call_release_testnet.py
# Enter APP_ID and mnemonic when prompted
```

## 📋 Your TestNet Address
```
SXIEIE2D7FOKUNQXUFUZIRYKE75RYD5KBN5BOYZFXLIL7LOTFX4VK3U7CE
```

## 🔗 Useful Links
- **TestNet Dispenser**: https://testnet.algoexplorer.io/dispenser
- **TestNet Explorer**: https://testnet.algoexplorer.io/
- **Pera Wallet**: https://perawallet.app/

## 🎯 Demo Flow
1. **Deploy**: `python deploy_with_address.py`
2. **Fund**: Send ALGO via Pera to app address
3. **Verify**: `python check_balance_testnet.py`
4. **Release**: `python call_release_testnet.py`
5. **Show**: All transactions on TestNet explorer

**Total demo time: 3-5 minutes** ⚡