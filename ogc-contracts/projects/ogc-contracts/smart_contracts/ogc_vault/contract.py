from pyteal import *
from beaker import *

class VaultState:
    goal = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("goal"), default=Int(0))
    deadline = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("deadline"), default=Int(0))
    receiver = GlobalStateValue(stack_type=TealType.bytes, key=Bytes("receiver"), default=Bytes(""))
    paused = GlobalStateValue(stack_type=TealType.uint64, key=Bytes("paused"), default=Int(0))

class VaultAccountState:
    contributed = LocalStateValue(stack_type=TealType.uint64, key=Bytes("contributed"), default=Int(0))

app = Application("OGC_Vault", state=VaultState, acct_state=VaultAccountState)

@app.create
def create(goal_amount: abi.Uint64, deadline_round: abi.Uint64, receiver_addr: abi.Address, *, output: abi.Uint64):
    return Seq(
        app.state.goal.set(goal_amount.get()),
        app.state.deadline.set(deadline_round.get()),
        app.state.receiver.set(receiver_addr.get()),
        app.state.paused.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.opt_in
def opt_in():
    return VaultAccountState.contributed.set(Int(0))

@Subroutine(TealType.none)
def _not_paused():
    return Assert(app.state.paused.get() == Int(0))

@app.external
def pause():
    return Seq(
        Assert(Txn.sender() == Global.creator_address()),
        app.state.paused.set(Int(1))
    )

@app.external
def unpause():
    return Seq(
        Assert(Txn.sender() == Global.creator_address()),
        app.state.paused.set(Int(0))
    )

@app.external
def contribute(payment: abi.PaymentTransaction):
    return Seq(
        _not_paused(),
        Assert(And(
            payment.get().receiver() == Global.current_application_address(),
            payment.get().amount() > Int(0),
        )),
        VaultAccountState.contributed.set(VaultAccountState.contributed.get() + payment.get().amount()),
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
            TxnField.receiver: app.state.receiver.get(),
            TxnField.amount: bal - Int(1_000_000),
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
        amt.store(VaultAccountState.contributed.get()),
        Assert(amt.load() > Int(0)),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: Txn.sender(),
            TxnField.amount: amt.load(),
        }),
        InnerTxnBuilder.Submit(),
        VaultAccountState.contributed.set(Int(0)),
    )
