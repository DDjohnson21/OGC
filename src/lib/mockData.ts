import { Trip, PendingAction, Contribution, User } from '@/types';
import { generateTripFromPlan } from './tripPlanner';

// Generate sample trips using the trip planner
const italyPlan = {
  name: 'Italy 2025',
  destination: 'italy',
  startDate: '2025-06-15',
  endDate: '2025-06-22',
  departureCity: 'new-york',
  groupSize: 4,
  contributionSchedule: 'weekly' as const,
  members: ['Alice', 'Bob', 'Charlie', 'Diana']
};

const japanPlan = {
  name: 'Japan Cherry Blossoms',
  destination: 'japan',
  startDate: '2025-04-10',
  endDate: '2025-04-17',
  departureCity: 'los-angeles',
  groupSize: 3,
  contributionSchedule: 'bi-weekly' as const,
  members: ['Eve', 'Frank', 'Grace']
};

const thailandPlan = {
  name: 'Thailand Adventure',
  destination: 'thailand',
  startDate: '2025-03-01',
  endDate: '2025-03-08',
  departureCity: 'miami',
  groupSize: 3,
  contributionSchedule: 'monthly' as const,
  members: ['Alice', 'Bob', 'Charlie']
};

export const mockTrips: Trip[] = [
  {
    ...generateTripFromPlan(italyPlan),
    id: 1,
    raised: 1860,
    nextDue: 'Fri • $25',
    status: '3/4 approvals',
    coverUrl: '/api/placeholder/300/200'
  },
  {
    ...generateTripFromPlan(japanPlan),
    id: 2,
    raised: 890,
    nextDue: 'Mon • $50',
    status: '2/3 approvals',
    coverUrl: '/api/placeholder/300/200'
  },
  {
    ...generateTripFromPlan(thailandPlan),
    id: 3,
    raised: 2000,
    nextDue: 'Complete',
    status: 'Goal reached!',
    coverUrl: '/api/placeholder/300/200'
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
