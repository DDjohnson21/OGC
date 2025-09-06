'use client'
import React from 'react';
import { ArrowLeft, Plus, CreditCard, MapPin, Calendar, Users, Search, Plane, Hotel, Car } from 'lucide-react';
import { Button, ProgressBar, Chip, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';
import { mockContributions, mockPendingActions } from '@/lib/mockData';
import { formatCurrency, getInitials } from '@/lib/utils';

export const TripDetailScreen: React.FC = () => {
  const { state, setCurrentScreen } = useApp();
  const { selectedTrip } = state;

  if (!selectedTrip) {
    setCurrentScreen('trip-list');
    return null;
  }

  const progressPercentage = Math.round((selectedTrip.raised / selectedTrip.goal) * 100);

  return (
    <div className="min-h-screen bg-white">
      {/* Header with Cover Image */}
      <div className="relative h-48 bg-gradient-to-r from-blue-400 to-purple-500">
        <button 
          onClick={() => setCurrentScreen('trip-list')}
          className="absolute top-4 left-4 p-2 bg-black/20 rounded-full text-white hover:bg-black/30 transition-colors"
        >
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="absolute bottom-4 left-4 text-white">
          <h1 className="text-2xl font-bold">{selectedTrip.name}</h1>
          <p className="text-lg">{formatCurrency(selectedTrip.raised)} / {formatCurrency(selectedTrip.goal)} USDC</p>
        </div>
      </div>

      <div className="p-6 pb-20">
        {/* Trip Info */}
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">
              {selectedTrip.departureCity} → {selectedTrip.destination}
            </span>
          </div>
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">
              {new Date(selectedTrip.startDate).toLocaleDateString()} - {new Date(selectedTrip.endDate).toLocaleDateString()}
            </span>
          </div>
          <div className="flex items-center gap-2 mb-4">
            <Users className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">
              {selectedTrip.groupSize} people • {selectedTrip.contributionSchedule} contributions
            </span>
          </div>
        </div>

        {/* Progress Section */}
        <div className="mb-6">
          <ProgressBar 
            current={selectedTrip.raised} 
            total={selectedTrip.goal} 
            className="mb-2" 
          />
          <p className="text-sm text-gray-600">{progressPercentage}% of goal reached</p>
          
          {progressPercentage < 100 && (
            <ChatBubble 
              message={`📊 You're ${progressPercentage}% of the way to your goal! Keep contributing to reach ${formatCurrency(selectedTrip.goal)}`}
              sender="system" 
              type="info"
              avatar="📊"
              name="OGC Assistant"
            />
          )}
          
          {progressPercentage >= 100 && (
            <ChatBubble 
              message="🎉 Congratulations! You've reached your funding goal! You can now book your trip."
              sender="system" 
              type="success"
              avatar="🎉"
              name="OGC Assistant"
            />
          )}
        </div>

        {/* Cost Breakdown */}
        {selectedTrip.estimatedCosts && (
          <div className="mb-6">
            <h3 className="font-semibold mb-3">Cost Breakdown</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center py-1">
                <span className="text-sm">✈️ Flights</span>
                <span className="text-sm font-medium">{formatCurrency(selectedTrip.estimatedCosts.flights)}</span>
              </div>
              <div className="flex justify-between items-center py-1">
                <span className="text-sm">🏨 Accommodation</span>
                <span className="text-sm font-medium">{formatCurrency(selectedTrip.estimatedCosts.accommodation)}</span>
              </div>
              <div className="flex justify-between items-center py-1">
                <span className="text-sm">🍽️ Food & Activities</span>
                <span className="text-sm font-medium">{formatCurrency(selectedTrip.estimatedCosts.food + selectedTrip.estimatedCosts.activities)}</span>
              </div>
              <div className="flex justify-between items-center py-1 border-t pt-2">
                <span className="font-medium">Total Goal</span>
                <span className="font-bold">{formatCurrency(selectedTrip.estimatedCosts.total)}</span>
              </div>
            </div>
          </div>
        )}

        {/* Members Section */}
        <div className="mb-6">
          <h3 className="font-semibold mb-3 flex items-center justify-between">
            Members
            <Chip variant="success">Approvals 3/4</Chip>
          </h3>
          <div className="flex items-center gap-3">
            <div className="flex -space-x-2">
              {selectedTrip.members.map((member, idx) => (
                <div 
                  key={idx} 
                  className="w-10 h-10 bg-blue-500 rounded-full border-2 border-white flex items-center justify-center text-white font-medium"
                >
                  {getInitials(member)}
                </div>
              ))}
            </div>
            <button className="w-10 h-10 border-2 border-dashed border-gray-300 rounded-full flex items-center justify-center text-gray-400 hover:border-gray-400 transition-colors">
              <Plus className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Travel Options Section */}
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Travel Planning</h3>
          <Button 
            variant="outline"
            className="w-full mb-4" 
            onClick={() => setCurrentScreen('travel-options')}
          >
            <Search className="w-4 h-4 mr-2" />
            Browse Travel Options
          </Button>
          
          {/* Selected Travel Options */}
          {((selectedTrip.selectedFlights?.length || 0) > 0 || 
            (selectedTrip.selectedHotels?.length || 0) > 0 || 
            (selectedTrip.selectedCars?.length || 0) > 0 || 
            (selectedTrip.selectedActivities?.length || 0) > 0) && (
            <div className="space-y-3">
              <h4 className="text-sm font-medium text-gray-700">Selected Options</h4>
              
              {(selectedTrip.selectedFlights?.length || 0) > 0 && (
                <div className="p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Plane className="w-4 h-4 text-blue-600" />
                    <span className="text-sm font-medium text-blue-800">Flights ({selectedTrip.selectedFlights?.length || 0})</span>
                  </div>
                  {selectedTrip.selectedFlights.map((flight, idx) => (
                    <div key={idx} className="text-xs text-blue-700">
                      {flight.airline} {flight.flightNumber} • {flight.departure.time} - {flight.arrival.time}
                    </div>
                  ))}
                </div>
              )}
              
              {(selectedTrip.selectedHotels?.length || 0) > 0 && (
                <div className="p-3 bg-green-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Hotel className="w-4 h-4 text-green-600" />
                    <span className="text-sm font-medium text-green-800">Hotels ({selectedTrip.selectedHotels?.length || 0})</span>
                  </div>
                  {selectedTrip.selectedHotels.map((hotel, idx) => (
                    <div key={idx} className="text-xs text-green-700">
                      {hotel.name} • {hotel.rating} stars
                    </div>
                  ))}
                </div>
              )}
              
              {(selectedTrip.selectedCars?.length || 0) > 0 && (
                <div className="p-3 bg-purple-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Car className="w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium text-purple-800">Cars ({selectedTrip.selectedCars?.length || 0})</span>
                  </div>
                  {selectedTrip.selectedCars.map((car, idx) => (
                    <div key={idx} className="text-xs text-purple-700">
                      {car.vehicle.make} {car.vehicle.model} • {car.company}
                    </div>
                  ))}
                </div>
              )}
              
              {(selectedTrip.selectedActivities?.length || 0) > 0 && (
                <div className="p-3 bg-orange-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <MapPin className="w-4 h-4 text-orange-600" />
                    <span className="text-sm font-medium text-orange-800">Activities ({selectedTrip.selectedActivities?.length || 0})</span>
                  </div>
                  {selectedTrip.selectedActivities.map((activity, idx) => (
                    <div key={idx} className="text-xs text-orange-700">
                      {activity.title} • {activity.duration}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Contributions Section */}
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Contributions</h3>
          <Button 
            className="w-full mb-4" 
            onClick={() => setCurrentScreen('contribute')}
          >
            Contribute {selectedTrip.weeklyAmount || 25} USDC
          </Button>
          <p className="text-sm text-gray-600 mb-3">Next due: {selectedTrip.nextDue}</p>
          
          <ChatBubble 
            message={`💳 Your next contribution of ${formatCurrency(selectedTrip.weeklyAmount || 25)} is due ${selectedTrip.nextDue}. Keep up the great progress!`}
            sender="system" 
            type="tip"
            avatar="💳"
            name="OGC Assistant"
          />
          
          <div className="space-y-2">
            {mockContributions.map((contribution) => (
              <div key={contribution.id} className="flex justify-between items-center py-2">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs ${
                    contribution.status === 'confirmed' ? 'bg-green-500' : 'bg-yellow-500'
                  }`}>
                    {getInitials(contribution.member)}
                  </div>
                  <span className="text-sm">{contribution.member} contributed</span>
                </div>
                <span className="text-sm font-medium">{formatCurrency(contribution.amount)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Pending Actions Section */}
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Actions Awaiting Approval</h3>
          {mockPendingActions.slice(0, 2).map((action) => (
            <button 
              key={action.id}
              onClick={() => setCurrentScreen('approvals')}
              className="w-full p-4 border border-gray-200 rounded-xl text-left hover:bg-gray-50 transition-colors mb-3"
            >
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">{action.type}: {formatCurrency(action.amount)} USDC</p>
                  <p className="text-sm text-gray-600">{action.description}</p>
                  <p className="text-xs text-blue-600 mt-1">{action.approvals}/{action.required} approvals</p>
                </div>
                <CreditCard className="w-5 h-5 text-gray-400" />
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Bottom Action Button */}
      <div className="fixed bottom-0 left-0 right-0 p-6 bg-white border-t">
        <Button 
          className="w-full" 
          onClick={() => setCurrentScreen('contribute')}
        >
          Contribute {selectedTrip.weeklyAmount || 25} USDC
        </Button>
      </div>
    </div>
  );
};
