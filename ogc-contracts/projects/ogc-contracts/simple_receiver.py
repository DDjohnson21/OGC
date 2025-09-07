#!/usr/bin/env python3
"""Simple ALGO Receiver Contract"""

from pyteal import *
from beaker import *

class ReceiverState:
    total_received = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("total"), default=Int(0))
    transaction_count = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("count"), default=Int(0))

app = Application("SimpleReceiver", state=ReceiverState)

@app.create
def create(*, output: abi.Uint64):
    return Seq(
        app.state.total_received.set(Int(0)),
        app.state.transaction_count.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.external
def receive_payment(payment: abi.PaymentTransaction):
    """Receives ALGO and logs it"""
    return Seq(
        # Verify payment is to this app
        Assert(And(
            payment.get().receiver() == Global.current_application_address(),
            payment.get().amount() > Int(0),
        )),
        
        # Update counters
        app.state.total_received.set(app.state.total_received.get() + payment.get().amount()),
        app.state.transaction_count.set(app.state.transaction_count.get() + Int(1)),
    )

@app.external(read_only=True)
def get_total(*, output: abi.Uint64):
    return output.set(app.state.total_received.get())

@app.external(read_only=True)
def get_count(*, output: abi.Uint64):
    return output.set(app.state.transaction_count.get())

if __name__ == "__main__":
    app.build().export("./artifacts/simple_receiver")