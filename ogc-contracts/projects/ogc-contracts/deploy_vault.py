#!/usr/bin/env python3
"""Deploy script for OGC Vault contract"""

from beaker import sandbox, client
from smart_contracts.ogc_vault.contract import app

def main():
    # Get sandbox client and account
    algod_client = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    
    # Deploy parameters
    goal = 1_000_000  # 1 ALGO goal
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 1000  # ~1 hour from now
    receiver = acct.address  # Use deployer as receiver for demo
    
    print(f"Deploying OGC Vault...")
    print(f"  Goal: {goal} microALGO ({goal/1_000_000} ALGO)")
    print(f"  Deadline: Round {deadline_round} (current: {current_round})")
    print(f"  Receiver: {receiver}")
    
    # Create the app
    app_client = client.ApplicationClient(
        client=algod_client,
        app=app,
        signer=acct.signer,
    )
    
    app_id, app_addr, _ = app_client.create(
        goal_amount=goal,
        deadline_round=deadline_round,
        receiver_addr=receiver,
    )
    
    print(f"\n✅ Deployed OGC Vault:")
    print(f"  APP_ID: {app_id}")
    print(f"  APP_ADDRESS: {app_addr}")
    print(f"\nNext steps:")
    print(f"1. Fund the app: python fund_app.py")
    print(f"2. Test contribute: python scripts/contribute.py")

if __name__ == "__main__":
    main()