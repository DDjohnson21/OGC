# OGC - Out The Group Chat

A travel fund management app built with React, TypeScript, and Tailwind CSS. OGC helps groups save money together for trips with transparent contributions and democratic decision-making.

## Features

### 🎯 Core Functionality
- **Group Trip Funding**: Create and manage trip funds with multiple members
- **Weekly Contributions**: Set up recurring contributions with customizable amounts
- **Democratic Approvals**: Require member consensus for withdrawals and payments
- **Real-time Progress**: Track funding progress with visual indicators
- **Wallet Integration**: Connect Algorand wallets for secure transactions

### 📱 Screens
1. **Splash/Onboarding**: Animated introduction with chat-style messaging
2. **Connect Wallet**: Algorand wallet connection (Pera, Defly) or demo mode
3. **Trip List**: Browse all active trip funds with search functionality
4. **Create Trip**: Multi-step wizard for setting up new trip funds
5. **Trip Detail**: Detailed view of trip progress, members, and contributions
6. **Contribute**: Modal for making contributions with amount presets
7. **Approvals**: Democratic voting system for trip actions
8. **Booking**: Mock travel booking integration with payment processing
9. **Map/Itinerary**: Interactive trip planning with checkable activities
10. **Profile**: User settings, trip history, and wallet management

### 🛠 Tech Stack
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Context API** for state management
- **Algorand** blockchain integration (mock)

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ocg
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
src/
├── components/
│   └── ui/                 # Reusable UI components
├── context/
│   └── AppContext.tsx      # Global state management
├── data/
│   └── mockData.ts         # Mock data for development
├── screens/                # Individual screen components
├── types/
│   └── index.ts           # TypeScript type definitions
├── utils/
│   └── index.ts           # Utility functions
├── App.tsx                # Main app component
├── main.tsx               # Entry point
└── index.css              # Global styles
```

## Key Features Explained

### Democratic Decision Making
- All major actions (withdrawals, payments) require 75% member approval
- Real-time approval tracking with visual progress indicators
- Transparent voting system with member avatars

### Wallet Integration
- Algorand blockchain for secure, low-fee transactions
- USDC ASA for stable value storage
- WalletConnect integration for easy connection

### User Experience
- Mobile-first responsive design
- Smooth animations and transitions
- Intuitive chat-style interface
- Real-time updates and notifications

## Development

### Adding New Screens
1. Create a new component in `src/screens/`
2. Add the screen type to `src/types/index.ts`
3. Update the `renderScreen` function in `src/App.tsx`
4. Add navigation logic as needed

### Styling
- Uses Tailwind CSS for utility-first styling
- Custom animations defined in `src/index.css`
- Component-specific styles using Tailwind classes

### State Management
- Context API for global state
- Local state for component-specific data
- Type-safe state updates with TypeScript

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Roadmap

- [ ] Real Algorand blockchain integration
- [ ] Bank account integration for auto-debits
- [ ] Push notifications for approvals
- [ ] Trip photo sharing
- [ ] Advanced itinerary planning
- [ ] Multi-currency support
- [ ] Trip expense tracking
- [ ] Social features and trip sharing
