'use client'

import React, { useState, useEffect } from 'react';
import { useApp } from '@/lib/context';
import { SplashScreen } from './screens/SplashScreen';
import { ConnectWalletScreen } from './screens/ConnectWalletScreen';
import { TripListScreen } from './screens/TripListScreen';
import { CreateTripScreen } from './screens/CreateTripScreen';
import { TripDetailScreen } from './screens/TripDetailScreen';
import { ContributeScreen } from './screens/ContributeScreen';
import { ApprovalsScreen } from './screens/ApprovalsScreen';
import { BookingScreen } from './screens/BookingScreen';
import { MapScreen } from './screens/MapScreen';
import { ProfileScreen } from './screens/ProfileScreen';
import { HowItWorksScreen } from './screens/HowItWorksScreen';
import { TravelOptionsScreen } from './screens/TravelOptionsScreen';

export const AppContent: React.FC = () => {
  const { state, setCurrentScreen } = useApp();
  const { currentScreen } = state;
  const [showDemoNavbar, setShowDemoNavbar] = useState(true);

  // Keyboard shortcut to toggle navbar (Ctrl/Cmd + D)
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
        event.preventDefault();
        setShowDemoNavbar(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const renderScreen = () => {
    switch (currentScreen) {
      case 'splash':
        return <SplashScreen />;
      case 'connect-wallet':
        return <ConnectWalletScreen />;
      case 'trip-list':
        return <TripListScreen />;
      case 'create-trip':
        return <CreateTripScreen />;
      case 'trip-detail':
        return <TripDetailScreen />;
      case 'contribute':
        return <ContributeScreen />;
      case 'approvals':
        return <ApprovalsScreen />;
      case 'booking':
        return <BookingScreen />;
      case 'map':
        return <MapScreen />;
      case 'profile':
        return <ProfileScreen />;
      case 'how-it-works':
        return <HowItWorksScreen />;
      case 'travel-options':
        return <TravelOptionsScreen />;
      default:
        return <SplashScreen />;
    }
  };

  return (
    <div className="font-sans min-h-screen">
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease-out forwards;
        }
        @keyframes typing {
          0%, 60%, 100% { opacity: 0; }
          30% { opacity: 1; }
        }
        .animate-typing {
          animation: typing 1.5s infinite;
        }
      `}</style>
      
      <div className={`${currentScreen !== 'splash' && currentScreen !== 'connect-wallet' && showDemoNavbar ? 'pt-16' : ''} min-h-screen`}>
        {renderScreen()}
      </div>
      
      {/* Demo Navbar for Video Recording */}
      {currentScreen !== 'splash' && currentScreen !== 'connect-wallet' && showDemoNavbar && (
        <div className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 px-4 py-3 z-50 shadow-sm">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <h1 className="text-lg font-semibold text-gray-900">OGC Demo</h1>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                <span className="text-xs text-gray-500">REC</span>
              </div>
            </div>
            <div className="flex items-center gap-1 lg:gap-2 overflow-x-auto">
              <button 
                onClick={() => setCurrentScreen('trip-list')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'trip-list' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Home
              </button>
              <button 
                onClick={() => setCurrentScreen('how-it-works')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'how-it-works' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                How It Works
              </button>
              <button 
                onClick={() => setCurrentScreen('create-trip')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'create-trip' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Create Trip
              </button>
              <button 
                onClick={() => setCurrentScreen('booking')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'booking' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Booking
              </button>
              <button 
                onClick={() => setCurrentScreen('map')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'map' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Map
              </button>
              <button 
                onClick={() => setCurrentScreen('profile')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'profile' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Profile
              </button>
              <button 
                onClick={() => setCurrentScreen('travel-options')} 
                className={`px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm transition-colors whitespace-nowrap ${
                  currentScreen === 'travel-options' 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Travel
              </button>
              <button 
                onClick={() => setShowDemoNavbar(false)}
                className="px-2 lg:px-3 py-1 rounded-full text-xs lg:text-sm bg-gray-200 text-gray-700 hover:bg-gray-300 transition-colors whitespace-nowrap"
              >
                Hide Nav
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Show Navbar Toggle Button */}
      {currentScreen !== 'splash' && currentScreen !== 'connect-wallet' && !showDemoNavbar && (
        <button
          onClick={() => setShowDemoNavbar(true)}
          className="fixed top-4 right-4 bg-blue-500 text-white px-3 py-2 rounded-full text-sm shadow-lg hover:bg-blue-600 transition-colors z-50"
          title="Press Ctrl+D to toggle navbar"
        >
          Show Nav
        </button>
      )}
      
      {/* Keyboard Shortcut Hint */}
      {currentScreen !== 'splash' && currentScreen !== 'connect-wallet' && showDemoNavbar && (
        <div className="fixed bottom-4 right-4 bg-black/80 text-white px-3 py-2 rounded-lg text-xs z-50">
          Press <kbd className="bg-white/20 px-1 rounded">Ctrl+D</kbd> to toggle navbar
        </div>
      )}
    </div>
  );
};

