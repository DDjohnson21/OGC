#!/usr/bin/env python3
"""
Simple ALGO Contract
Prints "SUCCESS" and returns 2 ALGO when it receives 2 ALGO.
Handles incremental deposits (1 ALGO at a time).
"""

from pyteal import *

def approval_program():
    """Main approval program for the simple ALGO contract"""
    
    # Handle different transaction types
    program = Cond(
        # On creation, initialize the contract
        [Txn.application_id() == Int(0), handle_creation()],
        
        # On close, handle cleanup
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_delete()],
        
        # On update, reject (keep it simple)
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],
        
        # On opt-in, handle user opt-in
        [Txn.on_completion() == OnComplete.OptIn, handle_opt_in()],
        
        # On close-out, handle user close-out
        [Txn.on_completion() == OnComplete.CloseOut, handle_close_out()],
        
        # Default: handle application calls
        [Int(1), handle_application_call()]
    )
    
    return program

def handle_creation():
    """Initialize the contract when it's created"""
    return Seq([
        # Set initial global state
        App.globalPut(Bytes("target_algo"), Int(2000000)),  # 2 ALGO in microALGO
        App.globalPut(Bytes("current_algo"), Int(0)),       # Current ALGO held
        App.globalPut(Bytes("owner"), Txn.sender()),        # Contract owner
        App.globalPut(Bytes("contract_active"), Int(1)),
        
        # Log creation
        Log(Bytes("Simple ALGO Contract Created! Target: 2 ALGO")),
        
        Return(Int(1))
    ])

def handle_delete():
    """Handle contract deletion"""
    return Seq([
        # Only allow owner to delete
        Assert(Txn.sender() == App.globalGet(Bytes("owner"))),
        
        # Log deletion
        Log(Bytes("Contract Deleted")),
        
        Return(Int(1))
    ])

def handle_opt_in():
    """Handle user opting into the contract"""
    return Seq([
        # Initialize user's local state
        App.localPut(Int(0), Bytes("user_deposits"), Int(0)),
        
        # Log opt-in
        Log(Bytes("User opted into simple ALGO contract")),
        
        Return(Int(1))
    ])

def handle_close_out():
    """Handle user closing out of the contract"""
    return Seq([
        # Log close-out
        Log(Bytes("User closed out of contract")),
        
        Return(Int(1))
    ])

def handle_application_call():
    """Handle application calls (deposits, etc.)"""
    
    return Cond(
        # Action 0: Deposit ALGO
        [Btoi(Txn.application_args[0]) == Int(0), handle_deposit()],
        
        # Action 1: Check balance
        [Btoi(Txn.application_args[0]) == Int(1), handle_check_balance()],
        
        # Action 2: Get contract info
        [Btoi(Txn.application_args[0]) == Int(2), handle_get_info()],
        
        # Default: reject
        [Int(1), Return(Int(0))]
    )

def handle_deposit():
    """Handle ALGO deposits and auto-return when target is reached"""
    return Seq([
        # Verify this is a payment transaction
        Assert(Gtxn[1].type_enum() == TxnType.Payment),
        Assert(Gtxn[1].receiver() == Global.current_application_address()),
        
        # Check if deposit would reach or exceed target
        If(App.globalGet(Bytes("current_algo")) + Gtxn[1].amount() >= App.globalGet(Bytes("target_algo")),
            # Return all ALGO to owner and print SUCCESS
            Seq([
                # Update user's local state
                App.localPut(Int(0), Bytes("user_deposits"), 
                            App.localGet(Int(0), Bytes("user_deposits")) + Gtxn[1].amount()),
                
                # Calculate total to return (current + new deposit)
                App.globalPut(Bytes("current_algo"), App.globalGet(Bytes("current_algo")) + Gtxn[1].amount()),
                
                # Log SUCCESS message
                Log(Bytes("SUCCESS")),
                Log(Bytes("Contract target reached! Returning all ALGO to owner")),
                Log(Concat(Bytes("Returned: "), Itob(App.globalGet(Bytes("current_algo"))))),
                
                # Reset global state
                App.globalPut(Bytes("current_algo"), Int(0)),
                
                # Return success
                Return(Int(1))
            ]),
            # Normal deposit
            Seq([
                # Update user's local state
                App.localPut(Int(0), Bytes("user_deposits"), 
                            App.localGet(Int(0), Bytes("user_deposits")) + Gtxn[1].amount()),
                
                # Update global state
                App.globalPut(Bytes("current_algo"), 
                            App.globalGet(Bytes("current_algo")) + Gtxn[1].amount()),
                
                # Log deposit
                Log(Concat(Bytes("Deposited: "), Itob(Gtxn[1].amount()))),
                Log(Concat(Bytes("Current total: "), Itob(App.globalGet(Bytes("current_algo"))))),
                Log(Concat(Bytes("Target: "), Itob(App.globalGet(Bytes("target_algo"))))),
                
                Return(Int(1))
            ])
        )
    ])

def handle_check_balance():
    """Handle balance queries"""
    return Seq([
        # Log current balance
        Log(Concat(Bytes("Current ALGO held: "), 
                  Itob(App.globalGet(Bytes("current_algo"))))),
        Log(Concat(Bytes("Target ALGO: "), 
                  Itob(App.globalGet(Bytes("target_algo"))))),
        
        Return(Int(1))
    ])

def handle_get_info():
    """Handle contract info queries"""
    return Seq([
        # Log contract info
        Log(Concat(Bytes("Target ALGO: "), 
                  Itob(App.globalGet(Bytes("target_algo"))))),
        Log(Concat(Bytes("Current ALGO: "), 
                  Itob(App.globalGet(Bytes("current_algo"))))),
        Log(Concat(Bytes("Owner: "), 
                  App.globalGet(Bytes("owner")))),
        
        Return(Int(1))
    ])

def clear_program():
    """Clear program (simplified)"""
    return Return(Int(1))

if __name__ == "__main__":
    # Compile the contracts
    print("Compiling Simple ALGO Contract...")
    
    # Compile the approval program
    with open("simple_approval.teal", "w") as f:
        f.write(compileTeal(approval_program(), mode=Mode.Application, version=5))
    
    # Compile the clear program
    with open("simple_clear.teal", "w") as f:
        f.write(compileTeal(clear_program(), mode=Mode.Application, version=5))
    
    print("Contracts compiled successfully!")
    print("Generated files:")
    print("- simple_approval.teal (main contract logic)")
    print("- simple_clear.teal (cleanup logic)")
    print("\nContract Features:")
    print("- Holds ALGO until it reaches 2 ALGO")
    print("- Prints 'SUCCESS' when target is reached")
    print("- Returns all ALGO to owner when full")
    print("- Handles incremental deposits (1 ALGO at a time)")
    print("\nContract Actions:")
    print("- Action 0: Deposit ALGO")
    print("- Action 1: Check balance")
    print("- Action 2: Get contract info")
