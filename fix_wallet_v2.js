const fs = require("fs");
const path = require("path");
const algosdk = require("algosdk");

const WALLET_PATH = path.join(__dirname, "permanent_wallet.json");
const BACKUP_PATH = path.join(__dirname, "permanent_wallet.backup.v2.json");

function toAddrString(addrOrObj) {
  if (!addrOrObj) return null;
  if (typeof addrOrObj === "string") return addrOrObj;
  // algosdk v4 Address object: try common shapes
  if (addrOrObj.publicKey instanceof Uint8Array) {
    return algosdk.encodeAddress(addrOrObj.publicKey);
  }
  if (addrOrObj.bytes instanceof Uint8Array) {
    return algosdk.encodeAddress(addrOrObj.bytes);
  }
  // Fallback: many v4 Address objects stringify nicely
  try { return String(addrOrObj); } catch (_) { return null; }
}

try {
  if (!fs.existsSync(WALLET_PATH)) throw new Error("permanent_wallet.json not found.");
  const j = JSON.parse(fs.readFileSync(WALLET_PATH, "utf8"));
  if (!j || typeof j !== "object") throw new Error("permanent_wallet.json is not valid JSON.");
  if (!j.mnemonic || typeof j.mnemonic !== "string") throw new Error("Missing 'mnemonic'.");

  const normalizedMnemonic = j.mnemonic.trim().replace(/\s+/g, " ");
  const acct = algosdk.mnemonicToSecretKey(normalizedMnemonic);

  // Derive address as a clean base32 string regardless of SDK
  const derivedAddr =
    typeof acct.addr === "string"
      ? acct.addr
      : toAddrString(acct.addr);

  if (!derivedAddr) {
    throw new Error("Could not derive address string from mnemonic.");
  }

  // If file has an object for addr, or a mismatched string, fix it
  const fileAddrStr = toAddrString(j.addr);
  if (fileAddrStr === derivedAddr) {
    console.log("Wallet file already consistent:");
    console.log("  Address:", derivedAddr);
    process.exit(0);
  }

  // Backup then overwrite with normalized values
  fs.copyFileSync(WALLET_PATH, BACKUP_PATH);
  console.log("Backed up existing file ->", BACKUP_PATH);

  const updated = {
    addr: derivedAddr,                // <-- string
    mnemonic: normalizedMnemonic,
    network: j.network || "testnet",
    note: "normalized by fix_wallet_v2.js",
  };
  fs.writeFileSync(WALLET_PATH, JSON.stringify(updated, null, 2));
  console.log("Updated permanent_wallet.json:");
  console.log("  Address:", derivedAddr);
  console.log("Done.");
} catch (e) {
  console.error(e.message || e);
  process.exit(1);
}