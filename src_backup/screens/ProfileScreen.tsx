import React from 'react';
import { ArrowLeft, Wallet, Settings, LogOut, Bell, DollarSign } from 'lucide-react';
import { Button, Chip } from '../components/ui';
import { useApp } from '../context/AppContext';
import { mockUser, mockTrips } from '../data/mockData';

export const ProfileScreen: React.FC = () => {
  const { state, setCurrentScreen, setWalletConnected, setUser } = useApp();
  const { user, walletConnected } = state;

  const handleLogout = () => {
    setWalletConnected(false);
    setUser(null);
    setCurrentScreen('splash');
  };

  const currentUser = user || mockUser;
  const userTrips = mockTrips.filter(trip => 
    trip.members.includes(currentUser.name)
  );

  return (
    <div className="min-h-screen bg-white p-6">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button onClick={() => setCurrentScreen('trip-list')}>
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold ml-4">Profile</h1>
      </div>

      {/* User Info */}
      <div className="text-center mb-8">
        <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
          {currentUser.avatar}
        </div>
        <h2 className="text-xl font-bold text-gray-900">{currentUser.name}</h2>
        {walletConnected && currentUser.walletAddress && (
          <p className="text-sm text-gray-600 mt-1">{currentUser.walletAddress}</p>
        )}
        <div className="mt-2">
          <Chip variant={walletConnected ? 'success' : 'default'}>
            {walletConnected ? 'Wallet Connected' : 'Demo Mode'}
          </Chip>
        </div>
      </div>

      {/* Trip Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="text-center p-4 bg-blue-50 rounded-xl">
          <p className="text-2xl font-bold text-blue-600">{userTrips.length}</p>
          <p className="text-sm text-gray-600">Trips Joined</p>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-xl">
          <p className="text-2xl font-bold text-green-600">
            ${userTrips.reduce((sum, trip) => sum + trip.raised, 0).toLocaleString()}
          </p>
          <p className="text-sm text-gray-600">Total Raised</p>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-xl">
          <p className="text-2xl font-bold text-purple-600">
            {userTrips.filter(trip => trip.status.includes('Goal reached')).length}
          </p>
          <p className="text-sm text-gray-600">Completed</p>
        </div>
      </div>

      {/* Settings Options */}
      <div className="space-y-4 mb-8">
        <h3 className="font-semibold text-gray-900">Settings</h3>
        
        <button className="w-full p-4 border border-gray-200 rounded-xl flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-3">
            <Wallet className="w-5 h-5 text-blue-500" />
            <span>Wallet Settings</span>
          </div>
          <span className="text-gray-400">›</span>
        </button>

        <button className="w-full p-4 border border-gray-200 rounded-xl flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-3">
            <Bell className="w-5 h-5 text-blue-500" />
            <span>Notifications</span>
          </div>
          <span className="text-gray-400">›</span>
        </button>

        <button className="w-full p-4 border border-gray-200 rounded-xl flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-3">
            <DollarSign className="w-5 h-5 text-blue-500" />
            <span>Currency & Region</span>
          </div>
          <span className="text-gray-400">›</span>
        </button>

        <button className="w-full p-4 border border-gray-200 rounded-xl flex items-center justify-between hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-3">
            <Settings className="w-5 h-5 text-blue-500" />
            <span>Privacy & Security</span>
          </div>
          <span className="text-gray-400">›</span>
        </button>
      </div>

      {/* My Trips */}
      <div className="mb-8">
        <h3 className="font-semibold text-gray-900 mb-4">My Trips</h3>
        <div className="space-y-3">
          {userTrips.map(trip => (
            <button 
              key={trip.id}
              onClick={() => setCurrentScreen('trip-detail')}
              className="w-full p-3 border border-gray-200 rounded-xl text-left hover:bg-gray-50 transition-colors"
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">{trip.name}</p>
                  <p className="text-sm text-gray-600">
                    ${trip.raised.toLocaleString()} / ${trip.goal.toLocaleString()}
                  </p>
                </div>
                <Chip variant={trip.status.includes('Goal reached') ? 'success' : 'default'}>
                  {trip.status}
                </Chip>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* App Info */}
      <div className="text-center text-sm text-gray-500 mb-8">
        <p>OGC v1.0.0</p>
        <p>Built on Algorand</p>
      </div>

      {/* Logout Button */}
      <Button 
        variant="outline" 
        className="w-full"
        onClick={handleLogout}
      >
        <LogOut className="w-4 h-4 mr-2" />
        {walletConnected ? 'Disconnect Wallet' : 'Exit Demo Mode'}
      </Button>
    </div>
  );
};
