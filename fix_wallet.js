const fs = require("fs");
const path = require("path");
const algosdk = require("algosdk");

const WALLET_PATH = path.join(__dirname, "permanent_wallet.json");
const BACKUP_PATH = path.join(__dirname, "permanent_wallet.backup.json");

function exit(msg) { console.error(msg); process.exit(1); }

try {
  if (!fs.existsSync(WALLET_PATH)) exit("permanent_wallet.json not found.");
  const j = JSON.parse(fs.readFileSync(WALLET_PATH, "utf8"));

  if (!j || typeof j !== "object") exit("permanent_wallet.json is not valid JSON.");
  if (!j.mnemonic || typeof j.mnemonic !== "string") exit("Missing 'mnemonic' in wallet file.");

  // Normalize whitespace in case of stray spaces/newlines
  const mnemonic = j.mnemonic.trim().replace(/\s+/g, " ");
  const acct = algosdk.mnemonicToSecretKey(mnemonic);

  if (!acct || !acct.addr) exit("Failed to derive account from mnemonic.");

  if (j.addr && j.addr === acct.addr) {
    console.log("Wallet file is already consistent:");
    console.log("  Address:", acct.addr);
    process.exit(0);
  }

  // Backup old file
  fs.copyFileSync(WALLET_PATH, BACKUP_PATH);
  console.log("Backed up existing file ->", BACKUP_PATH);

  // Overwrite with corrected addr (and normalized mnemonic)
  const updated = {
    addr: acct.addr,
    mnemonic,          // normalized 25-word phrase
    network: j.network || "testnet",
    note: "auto-fixed by fix_wallet.js"
  };
  fs.writeFileSync(WALLET_PATH, JSON.stringify(updated, null, 2));
  console.log("Updated permanent_wallet.json with correct address:");
  console.log("  Address:", acct.addr);
  console.log("Done.");
} catch (e) {
  console.error(e);
  process.exit(1);
}