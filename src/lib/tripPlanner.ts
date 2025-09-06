import { TripCosts, LocationData, NewTrip, Trip } from '@/types';

// Location data with cost multipliers
export const locationData: Record<string, LocationData> = {
  'italy': {
    name: 'Italy',
    country: 'Italy',
    currency: 'EUR',
    averageDailyCost: 120,
    flightCostMultiplier: 1.2,
    accommodationCostMultiplier: 1.0
  },
  'japan': {
    name: 'Japan',
    country: 'Japan',
    currency: 'JPY',
    averageDailyCost: 150,
    flightCostMultiplier: 1.8,
    accommodationCostMultiplier: 1.3
  },
  'thailand': {
    name: 'Thailand',
    country: 'Thailand',
    currency: 'THB',
    averageDailyCost: 60,
    flightCostMultiplier: 1.5,
    accommodationCostMultiplier: 0.6
  },
  'france': {
    name: 'France',
    country: 'France',
    currency: 'EUR',
    averageDailyCost: 130,
    flightCostMultiplier: 1.1,
    accommodationCostMultiplier: 1.1
  },
  'spain': {
    name: 'Spain',
    country: 'Spain',
    currency: 'EUR',
    averageDailyCost: 90,
    flightCostMultiplier: 1.0,
    accommodationCostMultiplier: 0.8
  },
  'greece': {
    name: 'Greece',
    country: 'Greece',
    currency: 'EUR',
    averageDailyCost: 80,
    flightCostMultiplier: 1.3,
    accommodationCostMultiplier: 0.7
  }
};

// Base costs from major US cities
const baseFlightCosts: Record<string, number> = {
  'new-york': 800,
  'los-angeles': 900,
  'chicago': 850,
  'miami': 750,
  'boston': 820,
  'seattle': 950,
  'atlanta': 780,
  'denver': 880
};

export function calculateTripCosts(
  destination: string,
  departureCity: string,
  startDate: string,
  endDate: string,
  groupSize: number
): TripCosts {
  const location = locationData[destination.toLowerCase()];
  if (!location) {
    throw new Error(`Location data not found for ${destination}`);
  }

  const start = new Date(startDate);
  const end = new Date(endDate);
  const tripDuration = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  
  // Calculate flight costs
  const baseFlightCost = baseFlightCosts[departureCity.toLowerCase()] || 800;
  const flightCost = Math.round(baseFlightCost * location.flightCostMultiplier * groupSize);
  
  // Calculate accommodation costs (per person per night)
  const accommodationPerNight = 80 * location.accommodationCostMultiplier;
  const accommodationCost = Math.round(accommodationPerNight * tripDuration * groupSize);
  
  // Calculate food costs (per person per day)
  const foodPerDay = 40;
  const foodCost = Math.round(foodPerDay * tripDuration * groupSize);
  
  // Calculate activities (per person per day)
  const activitiesPerDay = 60;
  const activitiesCost = Math.round(activitiesPerDay * tripDuration * groupSize);
  
  // Calculate local transportation
  const transportationPerDay = 25;
  const transportationCost = Math.round(transportationPerDay * tripDuration * groupSize);
  
  // Miscellaneous costs (10% of total)
  const subtotal = flightCost + accommodationCost + foodCost + activitiesCost + transportationCost;
  const miscellaneous = Math.round(subtotal * 0.1);
  
  const total = subtotal + miscellaneous;

  return {
    flights: flightCost,
    accommodation: accommodationCost,
    food: foodCost,
    activities: activitiesCost,
    transportation: transportationCost,
    miscellaneous: miscellaneous,
    total: total
  };
}

export function calculateContributionAmount(
  totalCost: number,
  contributionSchedule: 'weekly' | 'bi-weekly' | 'monthly',
  monthsToSave: number,
  groupSize: number
): number {
  const totalContributions = contributionSchedule === 'weekly' 
    ? monthsToSave * 4.33  // Average weeks per month
    : contributionSchedule === 'bi-weekly'
    ? monthsToSave * 2.17  // Average bi-weeks per month
    : monthsToSave;        // Monthly

  const amountPerPerson = totalCost / groupSize;
  const contributionAmount = Math.ceil(amountPerPerson / totalContributions);
  
  return contributionAmount;
}

export function calculateContributionAmounts(
  totalCost: number,
  monthsToSave: number,
  groupSize: number
): { weekly: number; biWeekly: number; monthly: number } {
  const amountPerPerson = totalCost / groupSize;
  
  const weeklyContributions = monthsToSave * 4.33;
  const biWeeklyContributions = monthsToSave * 2.17;
  const monthlyContributions = monthsToSave;
  
  return {
    weekly: Math.ceil(amountPerPerson / weeklyContributions),
    biWeekly: Math.ceil(amountPerPerson / biWeeklyContributions),
    monthly: Math.ceil(amountPerPerson / monthlyContributions)
  };
}

export function calculateMonthsToSave(startDate: string): number {
  const start = new Date(startDate);
  const now = new Date();
  const diffTime = start.getTime() - now.getTime();
  const diffMonths = Math.ceil(diffTime / (1000 * 60 * 60 * 24 * 30.44)); // Average days per month
  
  return Math.max(1, diffMonths); // At least 1 month
}

export function generateTripFromPlan(plan: NewTrip): Omit<Trip, 'id' | 'raised' | 'status' | 'nextDue' | 'coverUrl'> {
  const estimatedCosts = calculateTripCosts(
    plan.destination,
    plan.departureCity,
    plan.startDate,
    plan.endDate,
    plan.groupSize
  );
  
  const monthsToSave = calculateMonthsToSave(plan.startDate);
  const contributionAmount = calculateContributionAmount(
    estimatedCosts.total,
    plan.contributionSchedule,
    monthsToSave,
    plan.groupSize
  );

  return {
    name: plan.name,
    goal: estimatedCosts.total,
    members: plan.members,
    duration: Math.ceil((new Date(plan.endDate).getTime() - new Date(plan.startDate).getTime()) / (1000 * 60 * 60 * 24)),
    weeklyAmount: contributionAmount,
    destination: plan.destination,
    startDate: plan.startDate,
    endDate: plan.endDate,
    departureCity: plan.departureCity,
    groupSize: plan.groupSize,
    contributionSchedule: plan.contributionSchedule,
    estimatedCosts,
    contributionAmount,
    monthsToSave
  };
}

export function getPopularDestinations(): LocationData[] {
  return Object.values(locationData);
}

export function getDepartureCities(): string[] {
  return Object.keys(baseFlightCosts).map(city => 
    city.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
  );
}

export interface LocationRecommendation {
  type: 'flight' | 'hotel' | 'activity';
  name: string;
  description: string;
  price: string;
  rating?: number;
  icon: string;
  url?: string;
}

export function getLocationRecommendations(
  destination: string,
  departureCity: string,
  startDate: string,
  endDate: string,
  groupSize: number
): LocationRecommendation[] {
  const location = locationData[destination.toLowerCase()];
  if (!location) return [];

  const start = new Date(startDate);
  const end = new Date(endDate);
  const tripDuration = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
  
  const baseFlightCost = baseFlightCosts[departureCity.toLowerCase()] || 800;
  const flightCost = Math.round(baseFlightCost * location.flightCostMultiplier);
  const accommodationPerNight = 80 * location.accommodationCostMultiplier;

  const recommendations: LocationRecommendation[] = [
    // Flight recommendations
    {
      type: 'flight',
      name: `${departureCity} → ${location.name}`,
      description: `Round-trip flights for ${groupSize} people`,
      price: `$${flightCost * groupSize}`,
      rating: 4.5,
      icon: '✈️',
      url: '#'
    },
    {
      type: 'flight',
      name: 'Premium Airlines',
      description: 'Business class with extra legroom',
      price: `$${Math.round(flightCost * 1.8 * groupSize)}`,
      rating: 4.8,
      icon: '✈️',
      url: '#'
    },
    // Hotel recommendations
    {
      type: 'hotel',
      name: 'Budget Hotel',
      description: `${tripDuration} nights, ${groupSize} rooms`,
      price: `$${Math.round(accommodationPerNight * 0.7 * tripDuration * groupSize)}`,
      rating: 3.8,
      icon: '🏨',
      url: '#'
    },
    {
      type: 'hotel',
      name: 'Mid-range Hotel',
      description: `${tripDuration} nights, ${groupSize} rooms`,
      price: `$${Math.round(accommodationPerNight * tripDuration * groupSize)}`,
      rating: 4.2,
      icon: '🏨',
      url: '#'
    },
    {
      type: 'hotel',
      name: 'Luxury Resort',
      description: `${tripDuration} nights, ${groupSize} rooms`,
      price: `$${Math.round(accommodationPerNight * 1.8 * tripDuration * groupSize)}`,
      rating: 4.7,
      icon: '🏨',
      url: '#'
    },
    // Activity recommendations
    {
      type: 'activity',
      name: 'City Walking Tour',
      description: 'Guided tour of main attractions',
      price: `$${25 * groupSize}`,
      rating: 4.3,
      icon: '🚶‍♂️',
      url: '#'
    },
    {
      type: 'activity',
      name: 'Food & Wine Tasting',
      description: 'Local cuisine experience',
      price: `$${45 * groupSize}`,
      rating: 4.6,
      icon: '🍷',
      url: '#'
    },
    {
      type: 'activity',
      name: 'Adventure Activities',
      description: 'Hiking, biking, or water sports',
      price: `$${60 * groupSize}`,
      rating: 4.4,
      icon: '🏔️',
      url: '#'
    }
  ];

  return recommendations;
}

