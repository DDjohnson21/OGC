#!/usr/bin/env python3
"""ASA-compatible vault contract"""

from pyteal import *
from beaker import *

class ASAVaultState:
    goal = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("goal"), default=Int(0))
    deadline = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("deadline"), default=Int(0))
    receiver = GlobalStateValue(stack_type=TealType.bytes, key=Bytes("receiver"), default=Bytes(""))
    asset_id = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("asset_id"), default=Int(0))
    total = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("total"), default=Int(0))

app = Application("ASAVault", state=ASAVaultState)

@app.create
def create(goal_amount: abi.Uint64, deadline_round: abi.Uint64, receiver_addr: abi.Address, asset: abi.Asset, *, output: abi.Uint64):
    return Seq(
        app.state.goal.set(goal_amount.get()),
        app.state.deadline.set(deadline_round.get()),
        app.state.receiver.set(receiver_addr.get()),
        app.state.asset_id.set(asset.asset_id()),
        app.state.total.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.external
def contribute_asa(axfer: abi.AssetTransferTransaction):
    return Seq(
        Assert(And(
            axfer.get().xfer_asset() == app.state.asset_id.get(),
            axfer.get().asset_receiver() == Global.current_application_address(),
            axfer.get().asset_amount() > Int(0),
        )),
        app.state.total.set(app.state.total.get() + axfer.get().asset_amount()),
    )

@app.external
def release_asa():
    now = Global.round()
    return Seq(
        Assert(And(now >= app.state.deadline.get(), app.state.total.get() >= app.state.goal.get())),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.AssetTransfer,
            TxnField.xfer_asset: app.state.asset_id.get(),
            TxnField.asset_receiver: app.state.receiver.get(),
            TxnField.asset_amount: app.state.total.get(),
        }),
        InnerTxnBuilder.Submit(),
    )

@app.external(read_only=True)
def get_goal(*, output: abi.Uint64):
    return output.set(app.state.goal.get())

@app.external(read_only=True)
def get_total(*, output: abi.Uint64):
    return output.set(app.state.total.get())

@app.external(read_only=True)
def get_asset_id(*, output: abi.Uint64):
    return output.set(app.state.asset_id.get())

if __name__ == "__main__":
    app.build().export("./artifacts/asa_vault")