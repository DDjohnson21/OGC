import React from 'react';
import { ArrowLeft, Plus, CreditCard } from 'lucide-react';
import { Button, ProgressBar, Chip } from '../components/ui';
import { useApp } from '../context/AppContext';
import { mockContributions, mockPendingActions } from '../data/mockData';
import { formatCurrency, getInitials } from '../utils';

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
        {/* Progress Section */}
        <div className="mb-6">
          <ProgressBar 
            current={selectedTrip.raised} 
            total={selectedTrip.goal} 
            className="mb-2" 
          />
          <p className="text-sm text-gray-600">{progressPercentage}% of goal reached</p>
        </div>

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
