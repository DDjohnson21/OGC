#!/usr/bin/env python3
"""Deploy simple vault"""

from beaker import sandbox, client
from simple_vault import app

def main():
    algod_client = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    
    goal = 1_000_000  # 1 ALGO
    current_round = algod_client.status()["last-round"]
    deadline_round = current_round + 1000
    receiver = acct.address
    
    print(f"Deploying Simple Vault...")
    print(f"  Goal: {goal} microALGO")
    print(f"  Deadline: Round {deadline_round}")
    print(f"  Receiver: {receiver}")
    
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
    
    print(f"\n✅ Deployed Simple Vault:")
    print(f"  APP_ID: {app_id}")
    print(f"  APP_ADDRESS: {app_addr}")

if __name__ == "__main__":
    main()