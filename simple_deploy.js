// Deploys the TEAL app and writes simple_deployment.json with the appId
// Network: TestNet via Algonode (no token needed)

const fs = require("fs");
const path = require("path");
const algosdk = require("algosdk");

const ALGOD_URL = "https://testnet-api.algonode.cloud";
const ALGOD_TOKEN = ""; // not needed for Algonode
const ALGOD_PORT = "";

const APPROVAL_PATH = path.join(__dirname, "simple_approval.teal");
const CLEAR_PATH    = path.join(__dirname, "simple_clear.teal");
const WALLET_PATH   = path.join(__dirname, "permanent_wallet.json");
const OUT_PATH      = path.join(__dirname, "simple_deployment.json");

// --- Helpers ---------------------------------------------------------------

function deriveAddrStringFromAcct(acct) {
  // Normalize address across SDK v3/v4
  if (typeof acct.addr === "string") return acct.addr;
  if (acct.addr && acct.addr.publicKey instanceof Uint8Array) {
    return algosdk.encodeAddress(acct.addr.publicKey);
  }
  // Fallback (may be "[object Object]" in some builds; that's OK, we don't rely on it)
  return String(acct.addr);
}

function loadAccount() {
  const j = JSON.parse(fs.readFileSync(WALLET_PATH, "utf8"));
  if (!j || !j.mnemonic) throw new Error("permanent_wallet.json missing 'mnemonic'");
  if (!j.addr) throw new Error("permanent_wallet.json missing 'addr'");

  const acct = algosdk.mnemonicToSecretKey(j.mnemonic);
  const derived = deriveAddrStringFromAcct(acct);
  const fileAddr = String(j.addr).trim();

  // Validate the file address is a proper Algorand address
  if (!algosdk.isValidAddress(fileAddr)) {
    throw new Error(`'addr' in permanent_wallet.json is not a valid Algorand address: ${fileAddr}`);
  }

  // If they don't match, warn—but still use the file's string address (now known-good)
  if (derived !== fileAddr) {
    console.warn(
      "Warning: mnemonic-derived address != file address.\n" +
      `  derived: ${derived}\n` +
      `  file:    ${fileAddr}\n` +
      "Proceeding with the file address. If this persists, re-run fix_wallet_v2.js."
    );
  }

  // Return normalized shape: use the FILE string address as 'from'
  return { addr: fileAddr, sk: acct.sk };
}

async function compile(algod, tealSource) {
  const enc = new TextEncoder();
  const res = await algod.compile(enc.encode(tealSource)).do();
  return new Uint8Array(Buffer.from(res.result, "base64"));
}

// --- Main -----------------------------------------------------------------

async function main() {
  const algod = new algosdk.Algodv2(ALGOD_TOKEN, ALGOD_URL, ALGOD_PORT);
  const creator = loadAccount();

  const approvalTeal = fs.readFileSync(APPROVAL_PATH, "utf8");
  const clearTeal    = fs.readFileSync(CLEAR_PATH, "utf8");

  console.log("Compiling TEAL...");
  const approvalProg = await compile(algod, approvalTeal);
  const clearProg    = await compile(algod, clearTeal);

  // Minimal schema: 1 local uint ("d"); no globals
  const localInts = 1, localBytes = 0, globalInts = 0, globalBytes = 0;

  // Extra safety: show which 'from' we will use
  console.log("Using sender address:", creator.addr);

  const sp = await algod.getTransactionParams().do();
  
  // Convert suggested params to v2 format
  const suggestedParams = {
    fee: Number(sp.fee),
    firstRound: Number(sp.firstRound),
    lastRound: Number(sp.lastRound),
    genesisID: sp.genesisID,
    genesisHash: sp.genesisHash
  };
  
  const txn = algosdk.makeApplicationCreateTxnFromObject({
    from: creator.addr, // <- guaranteed string
    suggestedParams: suggestedParams,
    onComplete: algosdk.OnApplicationComplete.NoOpOC,
    approvalProgram: approvalProg,
    clearProgram: clearProg,
    numLocalInts: localInts,
    numLocalByteSlices: localBytes,
    numGlobalInts: globalInts,
    numGlobalByteSlices: globalBytes,
  });

  const signed = txn.signTxn(creator.sk);
  const { txId } = await algod.sendRawTransaction(signed).do();
  console.log("Sent app create tx:", txId);

  const resp = await algosdk.waitForConfirmation(algod, txId, 4);
  const appId = resp["application-index"];
  if (!appId) throw new Error("No application-index in create confirmation!");

  const appAddr = algosdk.getApplicationAddress(appId);
  console.log("Deployed App ID:", appId);
  console.log("App Address:", appAddr);

  fs.writeFileSync(
    OUT_PATH,
    JSON.stringify({ appId, appAddress: appAddr, network: "testnet" }, null, 2)
  );
  console.log(`Wrote ${OUT_PATH}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});