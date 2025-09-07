#!/usr/bin/env python3
"""Contract that can send ALGO to any wallet"""

from pyteal import *
from beaker import *

class SenderState:
    owner = GlobalStateValue(stack_type=TealType.bytes, key=Bytes("owner"), default=Bytes(""))
    total_sent = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("sent"), default=Int(0))

app = Application("SenderContract", state=SenderState)

@app.create
def create(*, output: abi.Uint64):
    return Seq(
        app.state.owner.set(Txn.sender()),
        app.state.total_sent.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.external
def send_algo(recipient: abi.Address, amount: abi.Uint64):
    """Send ALGO to any address (only owner can call)"""
    return Seq(
        # Only owner can send
        Assert(Txn.sender() == app.state.owner.get()),
        
        # Send ALGO to recipient
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: recipient.get(),
            TxnField.amount: amount.get(),
        }),
        InnerTxnBuilder.Submit(),
        
        # Update total sent
        app.state.total_sent.set(app.state.total_sent.get() + amount.get()),
    )

@app.external(read_only=True)
def get_balance(*, output: abi.Uint64):
    return output.set(Balance(Global.current_application_address()))

@app.external(read_only=True)
def get_total_sent(*, output: abi.Uint64):
    return output.set(app.state.total_sent.get())

if __name__ == "__main__":
    app.build().export("./artifacts/sender_contract")