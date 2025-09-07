#!/usr/bin/env python3
"""Echo Contract - Automatically sends ALGO back when received"""

from pyteal import *
from beaker import *

class EchoState:
    total_received = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("total"), default=Int(0))
    last_sender = GlobalStateValue(stack_type=TealType.bytes, key=Bytes("sender"), default=Bytes(""))

app = Application("EchoContract", state=EchoState)

@app.create
def create(*, output: abi.Uint64):
    return Seq(
        app.state.total_received.set(Int(0)),
        app.state.last_sender.set(Bytes("")),
        output.set(Global.current_application_id()),
    )

@app.external
def echo_payment(payment: abi.PaymentTransaction):
    """Receives ALGO and immediately sends it back"""
    return Seq(
        # Verify payment is to this app
        Assert(And(
            payment.get().receiver() == Global.current_application_address(),
            payment.get().amount() > Int(0),
        )),
        
        # Update state
        app.state.total_received.set(app.state.total_received.get() + payment.get().amount()),
        app.state.last_sender.set(payment.get().sender()),
        
        # Send ALGO back to sender (minus fees)
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: payment.get().sender(),
            TxnField.amount: payment.get().amount() - Int(1000),  # Subtract 0.001 ALGO fee
        }),
        InnerTxnBuilder.Submit(),
    )

@app.external(read_only=True)
def get_total(*, output: abi.Uint64):
    return output.set(app.state.total_received.get())

@app.external(read_only=True)
def get_last_sender(*, output: abi.String):
    return output.set(app.state.last_sender.get())

if __name__ == "__main__":
    app.build().export("./artifacts/echo_contract")