'use client'
import React from 'react';
import { Plus, Search, Plane } from 'lucide-react';
import { ProgressBar, Chip, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';
import { mockTrips } from '@/lib/mockData';
import { formatCurrency, getInitials } from '@/lib/utils';

export const TripListScreen: React.FC = () => {
  const { setCurrentScreen, setSelectedTrip } = useApp();

  const handleTripClick = (trip: typeof mockTrips[0]) => {
    setSelectedTrip(trip);
    setCurrentScreen('trip-detail');
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="p-4 lg:p-6 pb-20">
        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <Plane className="w-8 h-8 text-blue-500" />
          <h1 className="text-2xl font-bold text-black">Out The Group Chat</h1>
        </div>
        
        {/* Search Bar */}
        <div className="relative mb-6">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input 
            placeholder="Search trips..."
            className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Trip Cards */}
        <div className="space-y-4 lg:grid lg:grid-cols-2 lg:gap-6 lg:space-y-0">
          {mockTrips.map(trip => (
            <div 
              key={trip.id}
              onClick={() => handleTripClick(trip)}
              className="p-4 border border-gray-200 rounded-xl hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-semibold text-lg">{trip.name}</h3>
                <Chip variant={trip.status.includes('Goal reached') ? 'success' : 'default'}>
                  {trip.status}
                </Chip>
              </div>
              
              <div className="mb-3">
                <div className="flex justify-between text-sm text-gray-600 mb-1">
                  <span>{formatCurrency(trip.raised)} raised</span>
                  <span>{formatCurrency(trip.goal)} goal</span>
                </div>
                <ProgressBar current={trip.raised} total={trip.goal} />
              </div>
              
              <div className="flex justify-between items-center">
                <div className="flex -space-x-2">
                  {trip.members.slice(0, 3).map((member, idx) => (
                    <div 
                      key={idx} 
                      className="w-8 h-8 bg-blue-500 rounded-full border-2 border-white flex items-center justify-center text-white text-xs font-medium"
                    >
                      {getInitials(member)}
                    </div>
                  ))}
                  {trip.members.length > 3 && (
                    <div className="w-8 h-8 bg-gray-300 rounded-full border-2 border-white flex items-center justify-center text-gray-600 text-xs">
                      +{trip.members.length - 3}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">{trip.nextDue}</div>
                  <div className="text-xs text-gray-500">
                    {formatCurrency(trip.contributionAmount)} {trip.contributionSchedule}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State */}
        {mockTrips.length === 0 && (
          <div className="text-center py-12">
            <ChatBubble message="Start your first trip fund ✈️" sender="left" />
          </div>
        )}
      </div>

      {/* Floating Action Button */}
      <button 
        onClick={() => setCurrentScreen('create-trip')}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition-all flex items-center justify-center"
      >
        <Plus className="w-6 h-6" />
      </button>
    </div>
  );
};
