# OGC - Out The Groupchat 🚀

**Decentralized Group Funding on Algorand**

A hackathon project that solves the classic group coordination problem: "Who's actually going to pay?" 

## 💡 The Problem

We've all been there:
- Group chat: "Let's book that Airbnb!"
- Everyone: "I'm in!"
- Reality: Only 3 people actually pay, trip cancelled 😔

## ✨ The Solution

**OGC** creates trustless, goal-based funding pools on Algorand:
- Set a funding goal and deadline
- Everyone contributes to a smart contract
- Funds only release when goal is met
- If goal fails, everyone gets refunded automatically

## 🏗️ How It Works

```
1. Create Fund → Smart contract deployed with goal & deadline
2. Share Link → Friends contribute directly to contract  
3. Goal Met? → Funds released to organizer
4. Goal Failed? → Everyone gets refunded automatically
```

## 🧪 Testing

Run the complete demo:
```bash
# Activate environment
source venv/bin/activate

# Run hackathon demo
python ogc_demo.py

# Run comprehensive tests
python test_vault.py
```

## 📊 Demo Results

```
🎫 Concert Fund Example:
   Target: 50.0 ALGO
   Alice contributes: 15.0 ALGO
   Bob contributes: 20.0 ALGO  
   Charlie contributes: 15.0 ALGO
   
🎉 SUCCESS! Goal reached!
   Smart Contract: APP_ID 1020
   Total Raised: 50.0 ALGO
```

## 🔧 Technical Stack

- **Blockchain**: Algorand
- **Smart Contracts**: PyTeal + Beaker
- **Language**: Python
- **Testing**: LocalNet sandbox

## 🚀 Features

- ✅ **Trustless**: No central authority needed
- ✅ **Transparent**: All transactions on-chain
- ✅ **Secure**: Funds locked until conditions met
- ✅ **Automatic**: Refunds if goal not reached
- ✅ **Decentralized**: Runs entirely on Algorand

## 📁 Project Structure

```
ogc-contracts/
├── working_vault.py      # Main smart contract
├── deploy_working.py     # Deployment script
├── ogc_demo.py          # Hackathon demo
├── test_vault.py        # Test suite
└── artifacts/           # Compiled contracts
```

## 🎯 Use Cases

- **Group Travel**: Airbnb, flights, activities
- **Event Planning**: Concert tickets, restaurant bookings
- **Shared Purchases**: Group gifts, bulk orders
- **Community Projects**: Local initiatives, fundraising

## 🏆 Hackathon Highlights

- **Problem**: Group coordination & payment trust
- **Solution**: Algorand smart contract escrow
- **Innovation**: Automatic goal-based fund management
- **Impact**: Eliminates payment coordination friction

## 🔮 Future Roadmap

- [ ] Web frontend with Pera Wallet integration
- [ ] Mobile app for easy group creation
- [ ] Multi-token support (ASAs)
- [ ] Recurring payment schedules
- [ ] Integration with group chat platforms

---

**Built for Algorand Hackathon** 🏗️  
*Making group coordination trustless, one fund at a time*