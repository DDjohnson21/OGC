#!/usr/bin/env node
/**
 * Simple Reusable Wallet Manager
 * 
 * Creates and manages a permanent wallet address for ALGO transactions.
 */

const algosdk = require('algosdk');
const fs = require('fs');

// Algorand Testnet configuration
const ALGOD_TOKEN = '';
const ALGOD_SERVER = 'https://testnet-api.algonode.cloud';
const ALGOD_PORT = '';

// Create Algod client
const algodClient = new algosdk.Algodv2(ALGOD_TOKEN, ALGOD_SERVER, ALGOD_PORT);

const WALLET_FILE = 'permanent_wallet.json';

function createPermanentWallet() {
    console.log('🔑 Creating permanent wallet...');
    
    const account = algosdk.generateAccount();
    const address = account.addr;
    const mnemonic = algosdk.secretKeyToMnemonic(account.sk);
    
    const wallet = {
        address: address,
        mnemonic: mnemonic,
        privateKey: Array.from(account.sk),
        createdAt: new Date().toISOString(),
        type: 'permanent'
    };
    
    // Save wallet to file
    fs.writeFileSync(WALLET_FILE, JSON.stringify(wallet, null, 2));
    
    console.log('✅ Permanent wallet created!');
    console.log(`📍 Address: ${address}`);
    console.log(`🔐 Mnemonic: ${mnemonic}`);
    console.log(`💾 Saved to: ${WALLET_FILE}`);
    console.log('\n⚠️  IMPORTANT: Save this mnemonic safely!');
    console.log('   This is your permanent wallet address.');
    
    return wallet;
}

function loadPermanentWallet() {
    if (!fs.existsSync(WALLET_FILE)) {
        console.log('❌ No permanent wallet found. Creating new one...');
        return createPermanentWallet();
    }
    
    try {
        const walletData = fs.readFileSync(WALLET_FILE, 'utf8');
        const wallet = JSON.parse(walletData);
        
        // Handle different wallet file formats
        const address = wallet.address || wallet.addr;
        const createdAt = wallet.createdAt || wallet.note || 'Unknown';
        
        console.log('✅ Permanent wallet loaded!');
        console.log(`📍 Address: ${address}`);
        console.log(`📅 Created: ${createdAt}`);
        
        // Normalize wallet format
        return {
            address: address,
            addr: address, // Keep both for compatibility
            mnemonic: wallet.mnemonic,
            privateKey: wallet.privateKey,
            createdAt: createdAt,
            type: wallet.type || 'permanent'
        };
    } catch (error) {
        console.log('❌ Error loading wallet. Creating new one...');
        return createPermanentWallet();
    }
}

function getAccountFromWallet(wallet) {
    // If we have privateKey array, use it; otherwise derive from mnemonic
    let privateKey;
    if (wallet.privateKey && Array.isArray(wallet.privateKey)) {
        privateKey = new Uint8Array(wallet.privateKey);
    } else if (wallet.mnemonic) {
        const account = algosdk.mnemonicToSecretKey(wallet.mnemonic);
        privateKey = account.sk;
    } else {
        throw new Error('No private key or mnemonic found in wallet');
    }
    
    return {
        addr: wallet.address || wallet.addr,
        sk: privateKey
    };
}

async function checkBalance(address) {
    try {
        const accountInfo = await algodClient.accountInformation(address).do();
        const balance = Number(accountInfo.amount) / 1e6;
        return balance;
    } catch (error) {
        console.log('❌ Error checking balance:', error.message);
        return 0;
    }
}

async function fundWallet(wallet) {
    console.log('\n💰 Wallet Funding Instructions:');
    console.log(`📍 Your permanent wallet address: ${wallet.address}`);
    console.log('🔗 Go to: https://testnet.algoexplorer.io/dispenser');
    console.log('📝 Copy and paste your address above');
    console.log('💵 Request at least 10 ALGO (it\'s free!)');
    console.log('⏳ Press Enter when you have funded the wallet...');
    
    await new Promise(resolve => {
        process.stdin.once('data', () => resolve());
    });
    
    const balance = await checkBalance(wallet.address);
    console.log(`✅ Wallet balance: ${balance} ALGO`);
    
    if (balance < 1) {
        console.log('⚠️  Low balance! Please fund your wallet.');
        return false;
    }
    
    return true;
}

async function sendALGO(fromWallet, toAddress, amount) {
    try {
        console.log(`\n💸 Sending ${amount} ALGO to ${toAddress}...`);
        
        const account = getAccountFromWallet(fromWallet);
        const sp = await algodClient.getTransactionParams().do();
        
        // Convert to v2 format
        const suggestedParams = {
            fee: Number(sp.fee),
            firstRound: Number(sp.firstRound),
            lastRound: Number(sp.lastRound),
            genesisID: sp.genesisID,
            genesisHash: sp.genesisHash
        };
        
        const txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            from: account.addr,
            to: toAddress,
            amount: amount * 1e6, // Convert to microALGO
            suggestedParams: suggestedParams
        });
        
        const signedTxn = txn.signTxn(account.sk);
        const txId = await algodClient.sendRawTransaction(signedTxn).do();
        
        console.log(`📤 Transaction sent: ${txId}`);
        
        const result = await algosdk.waitForConfirmation(algodClient, txId, 4);
        console.log('✅ Transaction confirmed!');
        
        return txId;
    } catch (error) {
        console.error('❌ Error sending ALGO:', error.message);
        throw error;
    }
}

async function main() {
    try {
        console.log('🌟 Simple Reusable Wallet Manager\n');
        
        // Load or create permanent wallet
        const wallet = loadPermanentWallet();
        
        // Check current balance
        const balance = await checkBalance(wallet.address);
        console.log(`💰 Current balance: ${balance} ALGO`);
        
        if (balance < 1) {
            console.log('\n💳 Wallet needs funding...');
            const funded = await fundWallet(wallet);
            if (!funded) {
                console.log('❌ Please fund your wallet first.');
                return;
            }
        }
        
        console.log('\n🎯 Your Permanent Wallet:');
        console.log(`📍 Address: ${wallet.address}`);
        console.log(`💰 Balance: ${await checkBalance(wallet.address)} ALGO`);
        
        console.log('\n📋 Available Commands:');
        console.log('1. Check balance: node simple_wallet.js balance');
        console.log('2. Send ALGO: node simple_wallet.js send <address> <amount>');
        console.log('3. Fund wallet: node simple_wallet.js fund');
        
        // Handle command line arguments
        const args = process.argv.slice(2);
        
        if (args[0] === 'balance') {
            const balance = await checkBalance(wallet.address);
            console.log(`💰 Balance: ${balance} ALGO`);
        } else if (args[0] === 'send' && args[1] && args[2]) {
            const toAddress = args[1];
            const amount = parseFloat(args[2]);
            await sendALGO(wallet, toAddress, amount);
        } else if (args[0] === 'fund') {
            await fundWallet(wallet);
        } else {
            console.log('\n💡 Usage:');
            console.log('  node simple_wallet.js balance');
            console.log('  node simple_wallet.js send <address> <amount>');
            console.log('  node simple_wallet.js fund');
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

main();
