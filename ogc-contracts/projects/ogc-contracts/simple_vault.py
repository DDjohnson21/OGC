#!/usr/bin/env python3
"""Simple working vault contract"""

from pyteal import *
from beaker import *

# Simple vault without local state for now
app = Application("SimpleVault")

# Global state
goal = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("goal"), default=Int(0))
deadline = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("deadline"), default=Int(0))
receiver = GlobalStateValue(stack_type=TealType.bytes, key=Bytes("receiver"), default=Bytes(""))
total_contributed = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("total"), default=Int(0))

@app.create
def create(goal_amount: abi.Uint64, deadline_round: abi.Uint64, receiver_addr: abi.Address, *, output: abi.Uint64):
    return Seq(
        goal.set(goal_amount.get()),
        deadline.set(deadline_round.get()),
        receiver.set(receiver_addr.get()),
        total_contributed.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.external
def contribute(payment: abi.PaymentTransaction):
    return Seq(
        Assert(And(
            payment.get().receiver() == Global.current_application_address(),
            payment.get().amount() > Int(0),
        )),
        total_contributed.set(total_contributed.get() + payment.get().amount()),
    )

@app.external
def release():
    now = Global.round()
    bal = Balance(Global.current_application_address())
    return Seq(
        Assert(And(now >= deadline.get(), bal >= goal.get())),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: receiver.get(),
            TxnField.amount: bal - Int(1_000_000),
        }),
        InnerTxnBuilder.Submit(),
    )

@app.external(read_only=True)
def get_goal(*, output: abi.Uint64):
    return output.set(goal.get())

@app.external(read_only=True)
def get_total(*, output: abi.Uint64):
    return output.set(total_contributed.get())

if __name__ == "__main__":
    app.build().export("./artifacts/simple_vault")