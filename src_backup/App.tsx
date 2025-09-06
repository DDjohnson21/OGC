import React from 'react';
import { AppProvider, useApp } from './context/AppContext';
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

const AppContent: React.FC = () => {
  const { state, setCurrentScreen } = useApp();
  const { currentScreen } = state;

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
      default:
        return <SplashScreen />;
    }
  };

  return (
    <div className="font-sans">
      <style>{`
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
      
      {renderScreen()}
      
      {/* Demo Navigation - Hidden in production */}
      {currentScreen !== 'splash' && currentScreen !== 'connect-wallet' && (
        <div className="fixed bottom-4 left-4 bg-black/80 text-white p-2 rounded-lg text-xs space-y-1 z-50">
          <div>Demo Navigation:</div>
          <button 
            onClick={() => setCurrentScreen('trip-list')} 
            className="block hover:text-blue-300"
          >
            Home
          </button>
          <button 
            onClick={() => setCurrentScreen('booking')} 
            className="block hover:text-blue-300"
          >
            Booking
          </button>
          <button 
            onClick={() => setCurrentScreen('map')} 
            className="block hover:text-blue-300"
          >
            Map
          </button>
          <button 
            onClick={() => setCurrentScreen('profile')} 
            className="block hover:text-blue-300"
          >
            Profile
          </button>
        </div>
      )}
    </div>
  );
};

const App: React.FC = () => {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
};

export default App;
