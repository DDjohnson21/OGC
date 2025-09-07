#!/usr/bin/env python3
"""Get app address from APP_ID"""

from algosdk.logic import get_application_address

APP_ID = int(input("APP_ID: "))
app_addr = get_application_address(APP_ID)
print(f"APP_ADDRESS: {app_addr}")
print(f"Send ALGO to this address in Pera Wallet (TestNet)")