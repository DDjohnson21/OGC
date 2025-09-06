'use client'

import React, { useState, useEffect } from 'react';
import { ArrowLeft, X, Plus, Calendar, MapPin, Users, DollarSign } from 'lucide-react';
import { Button, Input, ChatBubble, Chip, Select, DatePicker, RecommendationsPanel } from '@/components/ui';
import { useApp } from '@/lib/context';
import { getPopularDestinations, getDepartureCities, calculateTripCosts, calculateContributionAmount, calculateContributionAmounts, calculateMonthsToSave } from '@/lib/tripPlanner';
import { formatCurrency } from '@/lib/utils';

export const CreateTripScreen: React.FC = () => {
  const { 
    state, 
    setCurrentScreen, 
    setCreateTripStep, 
    setNewTrip 
  } = useApp();

  const { createTripStep, newTrip } = state;
  const [estimatedCosts, setEstimatedCosts] = useState<any>(null);
  const [contributionAmount, setContributionAmount] = useState(0);
  const [contributionAmounts, setContributionAmounts] = useState({ weekly: 0, biWeekly: 0, monthly: 0 });

  const popularDestinations = getPopularDestinations();
  const departureCities = getDepartureCities();

  // Calculate costs when trip details change
  useEffect(() => {
    if (newTrip.destination && newTrip.departureCity && newTrip.startDate && newTrip.endDate && newTrip.groupSize) {
      try {
        const costs = calculateTripCosts(
          newTrip.destination,
          newTrip.departureCity,
          newTrip.startDate,
          newTrip.endDate,
          newTrip.groupSize
        );
        setEstimatedCosts(costs);

        const monthsToSave = calculateMonthsToSave(newTrip.startDate);
        const amount = calculateContributionAmount(
          costs.total,
          newTrip.contributionSchedule,
          monthsToSave,
          newTrip.groupSize
        );
        setContributionAmount(amount);

        // Calculate all contribution amounts
        const amounts = calculateContributionAmounts(
          costs.total,
          monthsToSave,
          newTrip.groupSize
        );
        setContributionAmounts(amounts);
      } catch (error) {
        console.error('Error calculating costs:', error);
      }
    }
  }, [newTrip.destination, newTrip.departureCity, newTrip.startDate, newTrip.endDate, newTrip.groupSize, newTrip.contributionSchedule]);

  const handleNext = () => {
    if (createTripStep < 4) {
      setCreateTripStep(createTripStep + 1);
    } else {
      // Create trip and go back to list
      setCurrentScreen('trip-list');
      setCreateTripStep(1);
      setNewTrip({ 
        name: '', 
        destination: '', 
        startDate: '', 
        endDate: '', 
        departureCity: '', 
        groupSize: 2, 
        contributionSchedule: 'weekly', 
        members: [] 
      });
    }
  };

  const handleBack = () => {
    if (createTripStep > 1) {
      setCreateTripStep(createTripStep - 1);
    } else {
      setCurrentScreen('trip-list');
    }
  };

  const addMember = (member: string) => {
    if (member.trim() && !newTrip.members.includes(member.trim())) {
      setNewTrip({
        ...newTrip,
        members: [...newTrip.members, member.trim()]
      });
    }
  };

  const removeMember = (index: number) => {
    setNewTrip({
      ...newTrip,
      members: newTrip.members.filter((_, i) => i !== index)
    });
  };

  const getScheduleLabel = (schedule: string) => {
    switch (schedule) {
      case 'weekly': return 'Weekly';
      case 'bi-weekly': return 'Bi-weekly';
      case 'monthly': return 'Monthly';
      default: return 'Weekly';
    }
  };

  return (
    <div className="min-h-screen bg-white p-4 lg:p-6">
      <div className="max-w-sm lg:max-w-2xl mx-auto">
        {/* Header */}
        <div className="flex items-center mb-6">
          <button onClick={handleBack}>
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-xl font-bold ml-4">Plan Your Trip</h1>
        </div>

        {/* Progress Bar */}
        <div className="flex items-center mb-8">
          {[1, 2, 3, 4].map((step) => (
            <div key={step} className="flex items-center">
              <div className={`flex-1 h-1 ${createTripStep >= step ? 'bg-blue-500' : 'bg-gray-200'} rounded-full`} />
              {step < 4 && <div className="w-2" />}
            </div>
          ))}
        </div>

        {/* Step 1: Destination & Dates */}
        {createTripStep === 1 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Where are you going?</h2>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Destination</label>
              <Select
                options={popularDestinations.map(dest => ({
                  value: dest.name.toLowerCase(),
                  label: dest.name,
                  description: dest.country,
                  icon: '🌍'
                }))}
                value={newTrip.destination}
                onChange={(value) => setNewTrip({...newTrip, destination: value})}
                placeholder="Select destination"
              />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
                <DatePicker
                  value={newTrip.startDate}
                  onChange={(value) => setNewTrip({...newTrip, startDate: value})}
                  placeholder="Select start date"
                  minDate={new Date().toISOString().split('T')[0]}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">End Date</label>
                <DatePicker
                  value={newTrip.endDate}
                  onChange={(value) => setNewTrip({...newTrip, endDate: value})}
                  placeholder="Select end date"
                  minDate={newTrip.startDate || new Date().toISOString().split('T')[0]}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Departing From</label>
              <Select
                options={departureCities.map(city => ({
                  value: city.toLowerCase().replace(' ', '-'),
                  label: city,
                  description: 'United States',
                  icon: '✈️'
                }))}
                value={newTrip.departureCity}
                onChange={(value) => setNewTrip({...newTrip, departureCity: value})}
                placeholder="Select departure city"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Group Size</label>
              <input
                type="number"
                min="1"
                max="20"
                value={newTrip.groupSize}
                onChange={(e) => setNewTrip({...newTrip, groupSize: parseInt(e.target.value) || 1})}
                className="w-full p-4 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              />
            </div>
          </div>
        )}

        {/* Step 2: Cost Breakdown & Recommendations */}
        {createTripStep === 2 && estimatedCosts && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Estimated Trip Costs</h2>
            
            <div className="p-4 bg-blue-50 rounded-xl">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-blue-600" />
                <span className="font-semibold text-blue-900">Total Estimated Cost</span>
              </div>
              <p className="text-2xl font-bold text-blue-600">{formatCurrency(estimatedCosts.total)}</p>
              <p className="text-sm text-blue-700">For {newTrip.groupSize} people</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">✈️ Flights</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.flights)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">🏨 Accommodation</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.accommodation)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">🍽️ Food & Dining</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.food)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">🎯 Activities</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.activities)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">🚗 Transportation</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.transportation)}</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <span className="text-sm">📱 Miscellaneous</span>
                <span className="font-medium">{formatCurrency(estimatedCosts.miscellaneous)}</span>
              </div>
            </div>

            {/* Live Travel Recommendations */}
            {newTrip.destination && newTrip.departureCity && newTrip.startDate && newTrip.endDate && (
              <RecommendationsPanel
                destination={newTrip.destination}
                departureCity={newTrip.departureCity}
                startDate={newTrip.startDate}
                endDate={newTrip.endDate}
                groupSize={newTrip.groupSize}
                tripId={1} // Demo trip ID
                className="mt-6"
                onSelectionChange={(type, selections) => {
                  // Update newTrip with selected options
                  const updatedTrip = {
                    ...newTrip,
                    [`selected${type.charAt(0).toUpperCase() + type.slice(1)}`]: selections
                  } as any;
                  setNewTrip(updatedTrip);
                }}
              />
            )}

            <ChatBubble 
              message="💡 Costs are estimated based on destination, group size, and travel dates. Actual costs may vary." 
              sender="system" 
              type="tip"
              avatar="💡"
              name="OGC Assistant"
            />
          </div>
        )}

        {/* Step 3: Contribution Schedule */}
        {createTripStep === 3 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">How often will you contribute?</h2>
            
            <ChatBubble 
              message="💰 Choose how often you want to contribute to your trip fund. More frequent contributions mean smaller individual payments." 
              sender="system" 
              type="tip"
              avatar="💰"
              name="OGC Assistant"
            />
            
            <div className="space-y-3">
              {(['weekly', 'bi-weekly', 'monthly'] as const).map((schedule) => {
                const amount = schedule === 'weekly' ? contributionAmounts.weekly :
                             schedule === 'bi-weekly' ? contributionAmounts.biWeekly :
                             contributionAmounts.monthly;
                
                return (
                  <button
                    key={schedule}
                    onClick={() => setNewTrip({...newTrip, contributionSchedule: schedule})}
                    className={`w-full p-4 border rounded-2xl text-left transition-all duration-200 ${
                      newTrip.contributionSchedule === schedule 
                        ? 'border-blue-500 bg-blue-50 text-blue-600 shadow-sm' 
                        : 'border-gray-200 hover:bg-gray-50 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium">{getScheduleLabel(schedule)}</p>
                        <p className="text-sm text-gray-600">
                          {schedule === 'weekly' && 'Every week'}
                          {schedule === 'bi-weekly' && 'Every 2 weeks'}
                          {schedule === 'monthly' && 'Every month'}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-lg">{formatCurrency(amount)}</p>
                        <p className="text-xs text-gray-500">per person</p>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>

            {contributionAmount > 0 && (
              <ChatBubble 
                message={`✅ You'll need to save ${formatCurrency(contributionAmount)} ${newTrip.contributionSchedule} per person\n\nTotal goal: ${formatCurrency(estimatedCosts?.total || 0)} • ${newTrip.groupSize} people • ${calculateMonthsToSave(newTrip.startDate)} months to save`}
                sender="system" 
                type="success"
                avatar="✅"
                name="OGC Assistant"
              />
            )}
          </div>
        )}

        {/* Step 4: Trip Name & Invite Members */}
        {createTripStep === 4 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Final Details</h2>
            
            <ChatBubble 
              message="📝 Give your trip a memorable name and invite your travel companions. They'll receive an invitation to join your group!" 
              sender="system" 
              type="tip"
              avatar="📝"
              name="OGC Assistant"
            />
            
            <Input
              placeholder="Trip name (e.g., Italy Summer 2025)"
              value={newTrip.name}
              onChange={(e) => setNewTrip({...newTrip, name: e.target.value})}
            />

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Invite Members</label>
              <div className="flex gap-2">
                <Input
                  placeholder="Email or username"
                  className="flex-1"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      addMember((e.target as HTMLInputElement).value);
                      (e.target as HTMLInputElement).value = '';
                    }
                  }}
                />
                <Button
                  onClick={() => {
                    const input = document.querySelector('input[placeholder="Email or username"]') as HTMLInputElement;
                    if (input) {
                      addMember(input.value);
                      input.value = '';
                    }
                  }}
                  className="px-4"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2">
              {newTrip.members.map((member, idx) => (
                <div key={idx} className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                  {member}
                  <button onClick={() => removeMember(idx)}>
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>

            <ChatBubble 
              message={`🎉 Trip Ready to Create!\n\n${newTrip.name || 'Your Trip'} • ${formatCurrency(estimatedCosts?.total || 0)} goal • ${formatCurrency(contributionAmount)} ${newTrip.contributionSchedule} per person`}
              sender="system" 
              type="success"
              avatar="🎉"
              name="OGC Assistant"
            />
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          {createTripStep > 1 && (
            <Button 
              variant="secondary"
              onClick={handleBack}
              className="flex-1 order-2 sm:order-1"
            >
              Back
            </Button>
          )}
          <Button 
            onClick={handleNext}
            className="flex-1 order-1 sm:order-2"
            disabled={
              (createTripStep === 1 && (!newTrip.destination || !newTrip.startDate || !newTrip.endDate || !newTrip.departureCity)) ||
              (createTripStep === 4 && !newTrip.name)
            }
          >
            {createTripStep === 4 ? 'Create Trip' : 'Next'}
          </Button>
        </div>
      </div>
    </div>
  );
};