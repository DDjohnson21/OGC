// Interacts with the app:
//   node simple_deposit.js optin
//   node simple_deposit.js deposit 1
//   node simple_deposit.js info
//
// Deposits must be grouped as [AppCall("deposit"), Payment], both from the same sender.
// When your cumulative deposits reach 2 ALGO, the app inner-sends 2 ALGO back and logs "success".

const fs = require("fs");
const path = require("path");
const algosdk = require("algosdk");

const ALGOD_URL = "https://testnet-api.algonode.cloud";
const ALGOD_TOKEN = ""; // not needed for Algonode
const ALGOD_PORT = "";

const WALLET_PATH = path.join(__dirname, "permanent_wallet.json");
const DEPLOY_PATH = path.join(__dirname, "simple_deployment.json");

// Normalize address across SDK v3/v4
function deriveAddr(acct) {
  if (typeof acct.addr === "string") return acct.addr;
  if (acct.addr && acct.addr.publicKey instanceof Uint8Array) {
    return algosdk.encodeAddress(acct.addr.publicKey);
  }
  return String(acct.addr);
}

function loadAccount() {
  const j = JSON.parse(fs.readFileSync(WALLET_PATH, "utf8"));
  const acct = algosdk.mnemonicToSecretKey(j.mnemonic);

  const derivedAddr = deriveAddr(acct);
  if (derivedAddr !== j.addr) {
    throw new Error("Wallet address does not match mnemonic in permanent_wallet.json");
  }
  return { addr: derivedAddr, sk: acct.sk };
}

function loadDeployment() {
  const j = JSON.parse(fs.readFileSync(DEPLOY_PATH, "utf8"));
  if (!j.appId) throw new Error("simple_deployment.json missing appId");
  return j;
}

function textArg(s) {
  return new Uint8Array(Buffer.from(s));
}

async function printLogsFromTx(algod, txId) {
  const conf = await algosdk.waitForConfirmation(algod, txId, 4);
  const logs = conf.logs || [];
  const dec = logs.map((b) => Buffer.from(b, "base64").toString("utf8"));
  if (dec.length) console.log("App Logs:", dec);
  // Show inner payments (e.g. 2 ALGO refund)
  if (conf["inner-txns"]) {
    conf["inner-txns"].forEach((itx, i) => {
      if (itx.txn && itx.txn.txn && itx.txn.txn.type === "pay") {
        const amt = itx.txn.txn.amt;
        const rcvr = algosdk.encodeAddress(new Uint8Array(itx.txn.txn.rcv));
        console.log(`Inner payment #${i}: ${amt} µALGO -> ${rcvr}`);
      }
    });
  }
  return conf;
}

async function doOptIn(algod, acct, appId) {
  const sp = await algod.getTransactionParams().do();
  const optin = algosdk.makeApplicationOptInTxnFromObject({
    from: acct.addr,
    appIndex: appId,
    suggestedParams: sp,
  });
  const signed = optin.signTxn(acct.sk);
  const { txId } = await algod.sendRawTransaction(signed).do();
  console.log("Sent opt-in tx:", txId);
  await algosdk.waitForConfirmation(algod, txId, 4);
  console.log("Opt-in confirmed");
}

async function doInfo(algod, acct, appId) {
  const sp = await algod.getTransactionParams().do();
  const call = algosdk.makeApplicationCallTxnFromObject({
    from: acct.addr,
    appIndex: appId,
    onComplete: algosdk.OnApplicationComplete.NoOpOC,
    suggestedParams: sp,
    appArgs: [textArg("info")],
  });
  const signed = call.signTxn(acct.sk);
  const { txId } = await algod.sendRawTransaction(signed).do();
  console.log("Sent info call tx:", txId);
  await printLogsFromTx(algod, txId);
}

async function doDeposit(algod, acct, appId, algos) {
  if (!Number.isFinite(algos) || algos <= 0) {
    throw new Error("Deposit amount must be a positive number of ALGOs");
  }
  const amount = Math.round(algos * 1_000_000);

  const sp = await algod.getTransactionParams().do();
  const appAddr = algosdk.getApplicationAddress(appId);

  // 1) App call first
  const appCallTxn = algosdk.makeApplicationCallTxnFromObject({
    from: acct.addr,
    appIndex: appId,
    onComplete: algosdk.OnApplicationComplete.NoOpOC,
    suggestedParams: sp,
    appArgs: [textArg("deposit")],
  });

  // 2) Payment second
  const payTxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
    from: acct.addr,
    to: appAddr,
    amount,
    suggestedParams: sp,
  });

  algosdk.assignGroupID([appCallTxn, payTxn]);

  const signed1 = appCallTxn.signTxn(acct.sk);
  const signed2 = payTxn.signTxn(acct.sk);

  const { txId } = await algod.sendRawTransaction([signed1, signed2]).do();
  console.log(`Sent grouped deposit txs. Group ID (first tx): ${txId}`);

  await printLogsFromTx(algod, txId);
}

async function main() {
  const [cmd, arg] = process.argv.slice(2);
  if (!cmd || !["optin", "deposit", "info"].includes(cmd)) {
    console.log("Usage:");
    console.log("  node simple_deposit.js optin");
    console.log("  node simple_deposit.js deposit 1");
    console.log("  node simple_deposit.js info");
    process.exit(1);
  }

  const algod = new algosdk.Algodv2(ALGOD_TOKEN, ALGOD_URL, ALGOD_PORT);
  const acct = loadAccount();
  const { appId } = loadDeployment();

  try {
    if (cmd === "optin") {
      await doOptIn(algod, acct, appId);
    } else if (cmd === "info") {
      await doInfo(algod, acct, appId);
    } else if (cmd === "deposit") {
      const amt = parseFloat(arg);
      if (!arg) throw new Error("Please provide an amount in ALGO, e.g. `deposit 1`");
      await doDeposit(algod, acct, appId, amt);
    }
  } catch (e) {
    const msg = String(e && e.message ? e.message : e);
    if (msg.toLowerCase().includes("already opted in")) {
      console.log("Already opted-in. You can proceed to deposit.");
      return;
    }
    console.error(e);
    process.exit(1);
  }
}

main();