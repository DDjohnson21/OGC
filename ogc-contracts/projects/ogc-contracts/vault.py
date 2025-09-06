# smart_contracts/vault.py
from pyteal import *
from beaker import *

class G:
    goal     = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))
    deadline = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))  # round #
    receiver = GlobalStateValue(stack_type=TealType.bytes,  default=Bytes(""))
    paused   = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))

class L:
    contributed = LocalStateValue(stack_type=TealType.uint64, default=Int(0))

app = Application("OGC_Vault", state=G(), acct_state=L())

@app.create
def create(goal: abi.Uint64, deadline_round: abi.Uint64, receiver: abi.Address, *, output: abi.Uint64):
    return Seq(
        app.state.goal.set(goal.get()),
        app.state.deadline.set(deadline_round.get()),
        app.state.receiver.set(receiver.get()),
        app.state.paused.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.opt_in
def opt_in():
    return app.acct_state.contributed.set(Int(0))

@Subroutine(TealType.none)
def _not_paused():
    return Assert(app.state.paused.get() == Int(0))

@app.external
def pause():
    return Assert(Txn.sender() == Global.creator_address(), app.state.paused.set(Int(1)))

@app.external
def unpause():
    return Assert(Txn.sender() == Global.creator_address(), app.state.paused.set(Int(0)))

@app.external
def contribute(*, pay: abi.PaymentTransaction):
    """Expect group: [ Payment->app , AppCall(contribute, pay=Gtxn[0]) ]"""
    return Seq(
        _not_paused(),
        Assert(And(
            pay.get().receiver() == Global.current_application_address(),
            pay.get().amount() > Int(0),
        )),
        app.acct_state.contributed.set(app.acct_state.contributed.get() + pay.get().amount()),
    )

@app.external
def release():
    now = Global.round()
    bal = Balance(Global.current_application_address())
    return Seq(
        Assert(And(now >= app.state.deadline.get(), bal >= app.state.goal.get())),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver:  app.state.receiver.get(),
            TxnField.amount:    bal - Int(1_000_000),  # leave min balance
        }),
        InnerTxnBuilder.Submit(),
    )

@app.external
def refund():
    now = Global.round()
    bal = Balance(Global.current_application_address())
    amt = ScratchVar(TealType.uint64)
    return Seq(
        Assert(And(now >= app.state.deadline.get(), bal < app.state.goal.get())),
        amt.store(app.acct_state.contributed.get()),
        Assert(amt.load() > Int(0)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver:  Txn.sender(),
            TxnField.amount:    amt.load(),
        }),
        InnerTxnBuilder.Submit(),
        app.acct_state.contributed.set(Int(0)),
    )

if __name__ == "__main__":
    app.build().export("./artifacts")
