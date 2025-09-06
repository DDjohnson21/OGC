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
  // New trip planning fields
  destination: string;
  startDate: string;
  endDate: string;
  departureCity: string;
  groupSize: number;
  contributionSchedule: 'weekly' | 'bi-weekly' | 'monthly';
  estimatedCosts: TripCosts;
  contributionAmount: number;
  monthsToSave: number;
  // Selected travel options
  selectedFlights?: any[];
  selectedHotels?: any[];
  selectedCars?: any[];
  selectedActivities?: any[];
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

export interface TripCosts {
  flights: number;
  accommodation: number;
  food: number;
  activities: number;
  transportation: number;
  miscellaneous: number;
  total: number;
}

export interface LocationData {
  name: string;
  country: string;
  currency: string;
  averageDailyCost: number;
  flightCostMultiplier: number;
  accommodationCostMultiplier: number;
}

export interface NewTrip {
  name: string;
  destination: string;
  startDate: string;
  endDate: string;
  departureCity: string;
  groupSize: number;
  contributionSchedule: 'weekly' | 'bi-weekly' | 'monthly';
  members: string[];
  coverImage?: string;
  selectedFlights?: any[];
  selectedHotels?: any[];
  selectedCars?: any[];
  selectedActivities?: any[];
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
  | 'profile'
  | 'how-it-works'
  | 'travel-options';

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
