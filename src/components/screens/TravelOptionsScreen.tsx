'use client'

import React, { useState } from 'react';
import { ArrowLeft, Search, Filter, MapPin, Calendar, Users } from 'lucide-react';
import { Button, RecommendationsPanel, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';

export const TravelOptionsScreen: React.FC = () => {
  const { setCurrentScreen, state, updateTripSelections } = useApp();
  const { selectedTrip } = state;
  
  const [searchParams, setSearchParams] = useState({
    destination: selectedTrip?.destination || '',
    departureCity: selectedTrip?.departureCity || '',
    startDate: selectedTrip?.startDate || '',
    endDate: selectedTrip?.endDate || '',
    groupSize: selectedTrip?.groupSize || 2
  });

  const handleBack = () => {
    setCurrentScreen('trip-detail');
  };

  const handleSearch = () => {
    // Trigger re-render of RecommendationsPanel with new params
    setSearchParams({ ...searchParams });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-4 sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <button onClick={handleBack} className="p-2 hover:bg-gray-100 rounded-full">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">Travel Options</h1>
            <p className="text-sm text-gray-600">Find flights, hotels, cars, and activities</p>
          </div>
        </div>
      </div>

      {/* Search Filters */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Destination</label>
            <input
              type="text"
              value={searchParams.destination}
              onChange={(e) => setSearchParams({...searchParams, destination: e.target.value})}
              placeholder="Where are you going?"
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Departing From</label>
            <input
              type="text"
              value={searchParams.departureCity}
              onChange={(e) => setSearchParams({...searchParams, departureCity: e.target.value})}
              placeholder="Departure city"
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
            <input
              type="date"
              value={searchParams.startDate}
              onChange={(e) => setSearchParams({...searchParams, startDate: e.target.value})}
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
            <input
              type="date"
              value={searchParams.endDate}
              onChange={(e) => setSearchParams({...searchParams, endDate: e.target.value})}
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Group Size</label>
            <input
              type="number"
              min="1"
              max="20"
              value={searchParams.groupSize}
              onChange={(e) => setSearchParams({...searchParams, groupSize: parseInt(e.target.value) || 1})}
              className="w-full p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex items-end">
            <Button onClick={handleSearch} className="w-full">
              <Search className="w-4 h-4 mr-2" />
              Search Options
            </Button>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="p-4 lg:p-6">
        <ChatBubble 
          message="🔍 Browse real-time travel options for your trip. Select flights, hotels, cars, and activities that work for your group!" 
          sender="system" 
          type="tip"
          avatar="🔍"
          name="OGC Assistant"
          className="mb-4"
        />
        
        <RecommendationsPanel
          destination={searchParams.destination}
          departureCity={searchParams.departureCity}
          startDate={searchParams.startDate}
          endDate={searchParams.endDate}
          groupSize={searchParams.groupSize}
          tripId={selectedTrip?.id}
          onSelectionChange={(type, selections) => {
            // Update trip selections in context and persist to localStorage
            if (selectedTrip) {
              updateTripSelections(selectedTrip.id, type, selections);
            }
          }}
        />
      </div>
    </div>
  );
};
