import logging
from beaker import sandbox
from smart_contracts.ogc_vault.contract import app

logger = logging.getLogger(__name__)

def deploy() -> None:
    # Get sandbox client and account
    algod_client = sandbox.get_algod_client()
    acct = sandbox.get_accounts().pop()
    
    # Deploy parameters
    goal = 1_000_000  # 1 ALGO goal
    deadline_round = algod_client.status()["last-round"] + 1000  # ~1 hour from now
    receiver = acct.address  # Use deployer as receiver for demo
    
    # Create the app
    app_id, app_addr, _ = app.create(
        sender=acct,
        suggested_params=algod_client.suggested_params(),
        goal=goal,
        deadline_round=deadline_round,
        receiver=receiver,
    )
    
    logger.info(f"Deployed OGC Vault:")
    logger.info(f"  APP_ID: {app_id}")
    logger.info(f"  APP_ADDRESS: {app_addr}")
    logger.info(f"  Goal: {goal} microALGO")
    logger.info(f"  Deadline: Round {deadline_round}")
    logger.info(f"  Receiver: {receiver}")
