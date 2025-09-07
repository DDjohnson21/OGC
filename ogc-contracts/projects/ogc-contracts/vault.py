# smart_contracts/vault.py
from pyteal import *
from beaker import *

class G:
    goal     = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))
    deadline = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))  # round #
    receiver = GlobalStateValue(stack_type=TealType.bytes,  default=Bytes(""))
    total    = GlobalStateValue(stack_type=TealType.uint64, default=Int(0))

app = Application("OGC_Vault", state=G())

@app.create
def create(goal: abi.Uint64, deadline_round: abi.Uint64, receiver: abi.Address, *, output: abi.Uint64):
    return Seq(
        app.state.goal.set(goal.get()),
        app.state.deadline.set(deadline_round.get()),
        app.state.receiver.set(receiver.get()),
        app.state.total.set(Int(0)),
        output.set(Global.current_application_id()),
    )

@app.external
def contribute(payment: abi.PaymentTransaction):
    return Seq(
        Assert(And(
            payment.get().receiver() == Global.current_application_address(),
            payment.get().amount() > Int(0),
        )),
        app.state.total.set(app.state.total.get() + payment.get().amount()),
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

@app.external(read_only=True)
def get_goal(*, output: abi.Uint64):
    return output.set(app.state.goal.get())

@app.external(read_only=True)
def get_total(*, output: abi.Uint64):
    return output.set(app.state.total.get())

if __name__ == "__main__":
    app.build().export("./artifacts")
