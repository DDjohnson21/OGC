export interface Trip {
  id: number;
  name: string;
  goal: number;
  raised: number;
  members: string[];
  nextDue: string;
  status: string;
  coverUrl: string;
  duration?: number;
  weeklyAmount?: number;
}

export interface PendingAction {
  id: number;
  type: 'Vendor Payment' | 'Withdraw' | 'Member Exit';
  amount: number;
  description: string;
  approvals: number;
  required: number;
  members: string[];
}

export interface Contribution {
  id: number;
  member: string;
  amount: number;
  date: string;
  status: 'pending' | 'confirmed';
}

export interface User {
  id: string;
  name: string;
  walletAddress?: string;
  avatar?: string;
}

export interface NewTrip {
  name: string;
  goal: string;
  duration: string;
  weeklyAmount: number;
  members: string[];
  coverImage?: string;
}

export interface Wallet {
  name: string;
  icon: string;
  connected: boolean;
}

export type Screen = 
  | 'splash'
  | 'connect-wallet'
  | 'trip-list'
  | 'create-trip'
  | 'trip-detail'
  | 'contribute'
  | 'approvals'
  | 'booking'
  | 'map'
  | 'profile';

export interface AppState {
  currentScreen: Screen;
  walletConnected: boolean;
  selectedTrip: Trip | null;
  createTripStep: number;
  newTrip: NewTrip;
  contributions: Record<number, boolean>;
  approvals: Record<number, boolean>;
  user: User | null;
}
