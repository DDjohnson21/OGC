import React from 'react';
import { ArrowLeft, X, Plus } from 'lucide-react';
import { Button, Input, ChatBubble } from '../components/ui';
import { useApp } from '../context/AppContext';

export const CreateTripScreen: React.FC = () => {
  const { 
    state, 
    setCurrentScreen, 
    setCreateTripStep, 
    setNewTrip 
  } = useApp();

  const { createTripStep, newTrip } = state;

  const handleNext = () => {
    if (createTripStep < 3) {
      setCreateTripStep(createTripStep + 1);
    } else {
      // Create trip and go back to list
      setCurrentScreen('trip-list');
      setCreateTripStep(1);
      setNewTrip({ name: '', goal: '', duration: '', weeklyAmount: 25, members: [] });
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

  return (
    <div className="min-h-screen bg-white p-6">
      <div className="max-w-sm mx-auto">
        {/* Header */}
        <div className="flex items-center mb-6">
          <button onClick={handleBack}>
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-xl font-bold ml-4">Create Trip</h1>
        </div>

        {/* Progress Bar */}
        <div className="flex items-center mb-8">
          <div className="flex-1 h-1 bg-blue-500 rounded-full" />
          <div className={`flex-1 h-1 ${createTripStep >= 2 ? 'bg-blue-500' : 'bg-gray-200'} rounded-full ml-2`} />
          <div className={`flex-1 h-1 ${createTripStep >= 3 ? 'bg-blue-500' : 'bg-gray-200'} rounded-full ml-2`} />
        </div>

        {/* Step 1: Trip Basics */}
        {createTripStep === 1 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Trip Basics</h2>
            
            <Input
              placeholder="Trip name"
              value={newTrip.name}
              onChange={(e) => setNewTrip({...newTrip, name: e.target.value})}
            />
            
            <Input
              placeholder="Goal amount (USDC)"
              type="number"
              value={newTrip.goal}
              onChange={(e) => setNewTrip({...newTrip, goal: e.target.value})}
            />
            
            <Input
              placeholder="Duration (weeks)"
              type="number"
              value={newTrip.duration}
              onChange={(e) => setNewTrip({...newTrip, duration: e.target.value})}
            />
            
            <div className="p-4 bg-gray-50 rounded-xl">
              <label className="block text-sm text-gray-600 mb-2">Cover Photo</label>
              <div className="w-full h-32 bg-gray-200 rounded-lg flex items-center justify-center text-gray-500 cursor-pointer hover:bg-gray-300 transition-colors">
                Click to upload
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Weekly Contributions */}
        {createTripStep === 2 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Weekly Contributions</h2>
            
            <div className="grid grid-cols-3 gap-3">
              {[10, 25, 50].map(amount => (
                <button
                  key={amount}
                  onClick={() => setNewTrip({...newTrip, weeklyAmount: amount})}
                  className={`p-3 rounded-xl border transition-colors ${
                    newTrip.weeklyAmount === amount 
                      ? 'border-blue-500 bg-blue-50 text-blue-600' 
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                >
                  ${amount}
                </button>
              ))}
            </div>
            
            <Input 
              placeholder="Custom amount"
              type="number"
              className="w-full"
            />
            
            <div className="p-4 bg-gray-50 rounded-xl">
              <label className="flex items-center gap-3">
                <input type="checkbox" disabled className="rounded" />
                <span className="text-gray-500">Bank weekly top-up (Phase 2)</span>
              </label>
              <ChatBubble message="Coming soon! Auto-debit from your bank." sender="left" />
            </div>
            
            <div className="text-sm text-gray-600">
              Network fee: ~$0.001 ALGO
            </div>
          </div>
        )}

        {/* Step 3: Invite Members */}
        {createTripStep === 3 && (
          <div className="space-y-6">
            <h2 className="text-lg font-semibold">Invite Members</h2>
            
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
            
            <div className="p-4 bg-green-50 rounded-xl">
              <p className="text-green-800 font-medium">Trip Created → {newTrip.name || 'Your Trip'}</p>
              <p className="text-green-600 text-sm mt-1">Ready to start collecting contributions!</p>
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex gap-4 mt-8">
          {createTripStep > 1 && (
            <Button 
              variant="secondary"
              onClick={handleBack}
              className="flex-1"
            >
              Back
            </Button>
          )}
          <Button 
            onClick={handleNext}
            className="flex-1"
            disabled={
              (createTripStep === 1 && (!newTrip.name || !newTrip.goal || !newTrip.duration)) ||
              (createTripStep === 2 && !newTrip.weeklyAmount)
            }
          >
            {createTripStep === 3 ? 'Create Trip' : 'Next'}
          </Button>
        </div>
      </div>
    </div>
  );
};
