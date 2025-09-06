'use client'

import React, { createContext, useContext, useReducer, ReactNode, useEffect } from 'react';
import { AppState, Screen, Trip, NewTrip, User } from '@/types';
import { storage } from './storage';

interface AppContextType {
  state: AppState;
  setCurrentScreen: (screen: Screen) => void;
  setWalletConnected: (connected: boolean) => void;
  setSelectedTrip: (trip: Trip | null) => void;
  setCreateTripStep: (step: number) => void;
  setNewTrip: (trip: NewTrip) => void;
  setContributions: (contributions: Record<number, boolean>) => void;
  setApprovals: (approvals: Record<number, boolean>) => void;
  setUser: (user: User | null) => void;
  updateTripSelections: (tripId: number, type: 'flights' | 'hotels' | 'cars' | 'activities', selections: any[]) => void;
  resetApp: () => void;
}

const getInitialState = (): AppState => {
  // Load from localStorage if available
  if (typeof window !== 'undefined' && storage.isAvailable()) {
    const savedSelectedTrip = storage.getSelectedTrip();
    const savedUserPreferences = storage.getUserPreferences();
    
    return {
      currentScreen: 'splash',
      walletConnected: savedUserPreferences.walletConnected || false,
      selectedTrip: savedSelectedTrip,
      createTripStep: 1,
      newTrip: { 
        name: '', 
        destination: '', 
        startDate: '', 
        endDate: '', 
        departureCity: '', 
        groupSize: 2, 
        contributionSchedule: 'weekly', 
        members: [] 
      },
      contributions: {},
      approvals: {},
      user: savedUserPreferences.user || null
    };
  }
  
  // Default state
  return {
    currentScreen: 'splash',
    walletConnected: false,
    selectedTrip: null,
    createTripStep: 1,
    newTrip: { 
      name: '', 
      destination: '', 
      startDate: '', 
      endDate: '', 
      departureCity: '', 
      groupSize: 2, 
      contributionSchedule: 'weekly', 
      members: [] 
    },
    contributions: {},
    approvals: {},
    user: null
  };
};

type AppAction = 
  | { type: 'SET_CURRENT_SCREEN'; payload: Screen }
  | { type: 'SET_WALLET_CONNECTED'; payload: boolean }
  | { type: 'SET_SELECTED_TRIP'; payload: Trip | null }
  | { type: 'SET_CREATE_TRIP_STEP'; payload: number }
  | { type: 'SET_NEW_TRIP'; payload: NewTrip }
  | { type: 'SET_CONTRIBUTIONS'; payload: Record<number, boolean> }
  | { type: 'SET_APPROVALS'; payload: Record<number, boolean> }
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'RESET_APP' };

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_CURRENT_SCREEN':
      return { ...state, currentScreen: action.payload };
    case 'SET_WALLET_CONNECTED':
      return { ...state, walletConnected: action.payload };
    case 'SET_SELECTED_TRIP':
      return { ...state, selectedTrip: action.payload };
    case 'SET_CREATE_TRIP_STEP':
      return { ...state, createTripStep: action.payload };
    case 'SET_NEW_TRIP':
      return { ...state, newTrip: action.payload };
    case 'SET_CONTRIBUTIONS':
      return { ...state, contributions: action.payload };
    case 'SET_APPROVALS':
      return { ...state, approvals: action.payload };
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'RESET_APP':
      return getInitialState();
    default:
      return state;
  }
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, getInitialState());

  const setCurrentScreen = (screen: Screen) => {
    dispatch({ type: 'SET_CURRENT_SCREEN', payload: screen });
  };

  const setWalletConnected = (connected: boolean) => {
    dispatch({ type: 'SET_WALLET_CONNECTED', payload: connected });
  };

  const setSelectedTrip = (trip: Trip | null) => {
    dispatch({ type: 'SET_SELECTED_TRIP', payload: trip });
    // Persist to localStorage
    if (typeof window !== 'undefined' && storage.isAvailable()) {
      storage.saveSelectedTrip(trip);
    }
  };

  const setCreateTripStep = (step: number) => {
    dispatch({ type: 'SET_CREATE_TRIP_STEP', payload: step });
  };

  const setNewTrip = (trip: NewTrip) => {
    dispatch({ type: 'SET_NEW_TRIP', payload: trip });
  };

  const setContributions = (contributions: Record<number, boolean>) => {
    dispatch({ type: 'SET_CONTRIBUTIONS', payload: contributions });
  };

  const setApprovals = (approvals: Record<number, boolean>) => {
    dispatch({ type: 'SET_APPROVALS', payload: approvals });
  };

  const setUser = (user: User | null) => {
    dispatch({ type: 'SET_USER', payload: user });
    // Persist user preferences
    if (typeof window !== 'undefined' && storage.isAvailable()) {
      storage.saveUserPreferences({ user, walletConnected: state.walletConnected });
    }
  };

  const updateTripSelections = (tripId: number, type: 'flights' | 'hotels' | 'cars' | 'activities', selections: any[]) => {
    // Update localStorage
    if (typeof window !== 'undefined' && storage.isAvailable()) {
      storage.updateTripSelections(tripId, type, selections);
    }
    
    // Update current selected trip if it matches
    if (state.selectedTrip && state.selectedTrip.id === tripId) {
      const updatedTrip = { ...state.selectedTrip };
      switch (type) {
        case 'flights':
          updatedTrip.selectedFlights = selections;
          break;
        case 'hotels':
          updatedTrip.selectedHotels = selections;
          break;
        case 'cars':
          updatedTrip.selectedCars = selections;
          break;
        case 'activities':
          updatedTrip.selectedActivities = selections;
          break;
      }
      setSelectedTrip(updatedTrip);
    }
  };

  const resetApp = () => {
    dispatch({ type: 'RESET_APP' });
    // Clear localStorage
    if (typeof window !== 'undefined' && storage.isAvailable()) {
      storage.clearAll();
    }
  };

  const value: AppContextType = {
    state,
    setCurrentScreen,
    setWalletConnected,
    setSelectedTrip,
    setCreateTripStep,
    setNewTrip,
    setContributions,
    setApprovals,
    setUser,
    updateTripSelections,
    resetApp
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
