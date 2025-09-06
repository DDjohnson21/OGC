import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { AppState, Screen, Trip, NewTrip, User } from '../types';

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
  resetApp: () => void;
}

const initialState: AppState = {
  currentScreen: 'splash',
  walletConnected: false,
  selectedTrip: null,
  createTripStep: 1,
  newTrip: { name: '', goal: '', duration: '', weeklyAmount: 25, members: [] },
  contributions: {},
  approvals: {},
  user: null
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
      return initialState;
    default:
      return state;
  }
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const setCurrentScreen = (screen: Screen) => {
    dispatch({ type: 'SET_CURRENT_SCREEN', payload: screen });
  };

  const setWalletConnected = (connected: boolean) => {
    dispatch({ type: 'SET_WALLET_CONNECTED', payload: connected });
  };

  const setSelectedTrip = (trip: Trip | null) => {
    dispatch({ type: 'SET_SELECTED_TRIP', payload: trip });
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
  };

  const resetApp = () => {
    dispatch({ type: 'RESET_APP' });
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
