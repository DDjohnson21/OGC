#!/usr/bin/env python3
"""Send ALGO from your wallet to any address"""

from algosdk.v2client import algod
from algosdk import mnemonic, transaction as tx
import algosdk

ALGOD_URL = "https://testnet-api.algonode.cloud"

def send_to_address():
    print("📤 Send ALGO to Any Address")
    
    # Option to use saved wallet or enter mnemonic
    print("1. Use saved wallet")
    print("2. Enter your own mnemonic")
    print("3. View saved wallet details")
    
    choice = input("Choose (1, 2, or 3): ").strip()
    
    if choice == "1":
        # Use the generated wallet
        mnemo = "swear suffer shrimp clinic cause differ nice space update mansion cradle brisk unknown lecture host clarify again faint divide decrease renew choice still abstract tomorrow"
        print("Using saved wallet: ZHMX3URT56ZLWQY3Y74CRXVOAVEOELOAVMXJZDT76IFORLPWMWMPJVAEN4")
    elif choice == "2":
        mnemo = input("Enter your 25-word mnemonic: ").strip()
    elif choice == "3":
        # View wallet details
        address = "ZHMX3URT56ZLWQY3Y74CRXVOAVEOELOAVMXJZDT76IFORLPWMWMPJVAEN4"
        mnemonic_saved = "swear suffer shrimp clinic cause differ nice space update mansion cradle brisk unknown lecture host clarify again faint divide decrease renew choice still abstract tomorrow"
        print(f"\n🔐 Saved Wallet Details:")
        print(f"Address: {address}")
        print(f"Mnemonic: {mnemonic_saved}")
        print(f"Explorer: https://testnet.algoexplorer.io/address/{address}")
        return
    else:
        print("❌ Invalid choice")
        return
    
    try:
        sk = mnemonic.to_private_key(mnemo)
        sender_addr = algosdk.account.address_from_private_key(sk)
        print(f"Sending from: {sender_addr}")
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        return
    
    # Get recipient and amount
    recipient = input("Paste recipient address: ").strip()
    amount_algo = float(input("Amount to send (ALGO): "))
    amount_micro = int(amount_algo * 1_000_000)
    
    # Connect to TestNet
    algod_client = algod.AlgodClient("", ALGOD_URL, "")
    
    try:
        # Check sender balance
        info = algod_client.account_info(sender_addr)
        balance = info["amount"] / 1_000_000
        print(f"Your balance: {balance} ALGO")
        
        if balance < amount_algo + 0.001:  # Need extra for fees
            print(f"❌ Insufficient balance. Need {amount_algo + 0.001} ALGO")
            return
        
        # Create and send transaction
        sp = algod_client.suggested_params()
        txn = tx.PaymentTxn(sender_addr, sp, recipient, amount_micro)
        stx = txn.sign(sk)
        txid = algod_client.send_transaction(stx)
        
        print(f"\n📤 Transaction sent!")
        print(f"   Amount: {amount_algo} ALGO")
        print(f"   To: {recipient}")
        print(f"   TX ID: {txid}")
        
        # Wait for confirmation
        print("Waiting for confirmation...")
        algosdk.transaction.wait_for_confirmation(algod_client, txid, 4)
        print(f"✅ SUCCESS! Transaction confirmed!")
        print(f"   Explorer: https://testnet.algoexplorer.io/tx/{txid}")
        
    except Exception as e:
        print(f"❌ Send failed: {e}")

if __name__ == "__main__":
    send_to_address()