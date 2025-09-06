import { Trip, PendingAction, Contribution, User } from '../types';

export const mockTrips: Trip[] = [
  {
    id: 1,
    name: 'Italy 2025',
    goal: 3000,
    raised: 1860,
    members: ['Alice', 'Bob', 'Charlie', 'Diana'],
    nextDue: 'Fri • $25',
    status: '3/4 approvals',
    coverUrl: '/api/placeholder/300/200',
    duration: 12,
    weeklyAmount: 25
  },
  {
    id: 2,
    name: 'Japan Cherry Blossoms',
    goal: 4500,
    raised: 890,
    members: ['Eve', 'Frank', 'Grace'],
    nextDue: 'Mon • $50',
    status: '2/3 approvals',
    coverUrl: '/api/placeholder/300/200',
    duration: 8,
    weeklyAmount: 50
  },
  {
    id: 3,
    name: 'Thailand Adventure',
    goal: 2000,
    raised: 2000,
    members: ['Alice', 'Bob', 'Charlie'],
    nextDue: 'Complete',
    status: 'Goal reached!',
    coverUrl: '/api/placeholder/300/200',
    duration: 6,
    weeklyAmount: 30
  }
];

export const mockPendingActions: PendingAction[] = [
  {
    id: 1,
    type: 'Vendor Payment',
    amount: 1200,
    description: 'Flight booking - Emirates',
    approvals: 3,
    required: 4,
    members: ['Alice', 'Bob', 'Charlie', 'Diana']
  },
  {
    id: 2,
    type: 'Withdraw',
    amount: 500,
    description: 'Emergency fund withdrawal',
    approvals: 2,
    required: 4,
    members: ['Alice', 'Bob', 'Charlie', 'Diana']
  },
  {
    id: 3,
    type: 'Member Exit',
    amount: 0,
    description: 'Grace wants to leave Japan trip',
    approvals: 1,
    required: 3,
    members: ['Eve', 'Frank', 'Grace']
  }
];

export const mockContributions: Contribution[] = [
  {
    id: 1,
    member: 'Alice',
    amount: 25,
    date: '2024-01-15',
    status: 'confirmed'
  },
  {
    id: 2,
    member: 'Bob',
    amount: 50,
    date: '2024-01-15',
    status: 'confirmed'
  },
  {
    id: 3,
    member: 'Charlie',
    amount: 25,
    date: '2024-01-14',
    status: 'confirmed'
  },
  {
    id: 4,
    member: 'Diana',
    amount: 25,
    date: '2024-01-14',
    status: 'pending'
  }
];

export const mockUser: User = {
  id: '1',
  name: 'Alice',
  walletAddress: '0x1234...5678',
  avatar: 'A'
};

export const mockWallets = [
  {
    name: 'Pera Wallet',
    icon: 'P',
    connected: false
  },
  {
    name: 'Defly',
    icon: 'D',
    connected: false
  }
];

export const onboardingMessages = [
  { text: 'Italy this summer 👀', sender: 'left' as const, delay: 0 },
  { text: 'Flights + hotel are like $3k…', sender: 'right' as const, delay: 1500 },
  { text: 'Trips always die in the group chat 😩', sender: 'left' as const, delay: 3000 },
  { text: 'Not anymore. Meet OGC.', sender: 'right' as const, delay: 4500, bold: true }
];
