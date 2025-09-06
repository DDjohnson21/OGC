// Local storage utilities for persisting trip data
import { Trip } from '@/types';

const STORAGE_KEYS = {
  TRIPS: 'ocg_trips',
  SELECTED_TRIP: 'ocg_selected_trip',
  USER_PREFERENCES: 'ocg_user_preferences'
} as const;

export class StorageService {
  // Trip management
  static saveTrips(trips: Trip[]): void {
    try {
      localStorage.setItem(STORAGE_KEYS.TRIPS, JSON.stringify(trips));
    } catch (error) {
      console.error('Error saving trips to localStorage:', error);
    }
  }

  static getTrips(): Trip[] {
    try {
      const trips = localStorage.getItem(STORAGE_KEYS.TRIPS);
      return trips ? JSON.parse(trips) : [];
    } catch (error) {
      console.error('Error loading trips from localStorage:', error);
      return [];
    }
  }

  static saveTrip(trip: Trip): void {
    try {
      const trips = this.getTrips();
      const existingIndex = trips.findIndex(t => t.id === trip.id);
      
      if (existingIndex >= 0) {
        trips[existingIndex] = trip;
      } else {
        trips.push(trip);
      }
      
      this.saveTrips(trips);
    } catch (error) {
      console.error('Error saving trip to localStorage:', error);
    }
  }

  static updateTripSelections(
    tripId: number, 
    type: 'flights' | 'hotels' | 'cars' | 'activities', 
    selections: any[]
  ): void {
    try {
      const trips = this.getTrips();
      const tripIndex = trips.findIndex(t => t.id === tripId);
      
      if (tripIndex >= 0) {
        const trip = trips[tripIndex];
        
        switch (type) {
          case 'flights':
            trip.selectedFlights = selections;
            break;
          case 'hotels':
            trip.selectedHotels = selections;
            break;
          case 'cars':
            trip.selectedCars = selections;
            break;
          case 'activities':
            trip.selectedActivities = selections;
            break;
        }
        
        trips[tripIndex] = trip;
        this.saveTrips(trips);
      }
    } catch (error) {
      console.error('Error updating trip selections:', error);
    }
  }

  static getTrip(tripId: number): Trip | null {
    try {
      const trips = this.getTrips();
      return trips.find(t => t.id === tripId) || null;
    } catch (error) {
      console.error('Error getting trip from localStorage:', error);
      return null;
    }
  }

  static deleteTrip(tripId: number): void {
    try {
      const trips = this.getTrips();
      const filteredTrips = trips.filter(t => t.id !== tripId);
      this.saveTrips(filteredTrips);
    } catch (error) {
      console.error('Error deleting trip from localStorage:', error);
    }
  }

  // Selected trip management
  static saveSelectedTrip(trip: Trip | null): void {
    try {
      if (trip) {
        localStorage.setItem(STORAGE_KEYS.SELECTED_TRIP, JSON.stringify(trip));
      } else {
        localStorage.removeItem(STORAGE_KEYS.SELECTED_TRIP);
      }
    } catch (error) {
      console.error('Error saving selected trip to localStorage:', error);
    }
  }

  static getSelectedTrip(): Trip | null {
    try {
      const trip = localStorage.getItem(STORAGE_KEYS.SELECTED_TRIP);
      return trip ? JSON.parse(trip) : null;
    } catch (error) {
      console.error('Error loading selected trip from localStorage:', error);
      return null;
    }
  }

  // User preferences
  static saveUserPreferences(preferences: any): void {
    try {
      localStorage.setItem(STORAGE_KEYS.USER_PREFERENCES, JSON.stringify(preferences));
    } catch (error) {
      console.error('Error saving user preferences to localStorage:', error);
    }
  }

  static getUserPreferences(): any {
    try {
      const preferences = localStorage.getItem(STORAGE_KEYS.USER_PREFERENCES);
      return preferences ? JSON.parse(preferences) : {};
    } catch (error) {
      console.error('Error loading user preferences from localStorage:', error);
      return {};
    }
  }

  // Clear all data
  static clearAll(): void {
    try {
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key);
      });
    } catch (error) {
      console.error('Error clearing localStorage:', error);
    }
  }

  // Check if localStorage is available
  static isAvailable(): boolean {
    try {
      const test = '__localStorage_test__';
      localStorage.setItem(test, test);
      localStorage.removeItem(test);
      return true;
    } catch {
      return false;
    }
  }
}

// Export singleton instance
export const storage = StorageService;
