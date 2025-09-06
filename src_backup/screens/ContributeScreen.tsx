import React, { useState } from 'react';
import { Button, Input } from '../components/ui';
import { useApp } from '../context/AppContext';

export const ContributeScreen: React.FC = () => {
  const { state, setCurrentScreen } = useApp();
  const { selectedTrip } = state;
  const [selectedAmount, setSelectedAmount] = useState(25);
  const [customAmount, setCustomAmount] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleContribute = async () => {
    setIsSubmitting(true);
    
    // Simulate transaction
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    setCurrentScreen('trip-detail');
    
    // Show success message
    setTimeout(() => {
      alert('Contribution sent ✅');
    }, 500);
  };

  const handleCancel = () => {
    setCurrentScreen('trip-detail');
  };

  const amount = customAmount ? parseInt(customAmount) : selectedAmount;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-end z-50">
      <div className="w-full bg-white rounded-t-3xl p-6 max-h-[80vh] overflow-y-auto">
        <div className="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-6" />
        
        <h2 className="text-xl font-bold mb-6">Contribute to {selectedTrip?.name}</h2>
        
        <div className="space-y-4 mb-6">
          {/* Amount Presets */}
          <div className="grid grid-cols-3 gap-3">
            {[10, 25, 50].map(amount => (
              <button
                key={amount}
                onClick={() => {
                  setSelectedAmount(amount);
                  setCustomAmount('');
                }}
                className={`p-3 rounded-xl border transition-colors ${
                  (customAmount ? false : selectedAmount === amount)
                    ? 'border-blue-500 bg-blue-50 text-blue-600' 
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
              >
                {amount} USDC
              </button>
            ))}
          </div>
          
          {/* Custom Amount */}
          <Input 
            placeholder="Custom amount"
            type="number"
            value={customAmount}
            onChange={(e) => {
              setCustomAmount(e.target.value);
              setSelectedAmount(0);
            }}
            className="w-full"
          />
          
          {/* Wallet Selection */}
          <select className="w-full p-4 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option>Wallet (USDCa)</option>
            <option disabled>Bank Account (Coming Soon)</option>
          </select>
          
          {/* Network Fee Info */}
          <div className="p-3 bg-gray-50 rounded-xl">
            <p className="text-sm text-gray-600">Network fee: ~$0.001 ALGO</p>
            <p className="text-xs text-gray-500 mt-1">Total: {amount} USDC + 0.001 ALGO</p>
          </div>
        </div>
        
        <div className="space-y-3">
          <Button 
            className="w-full"
            onClick={handleContribute}
            disabled={isSubmitting || amount <= 0}
          >
            {isSubmitting ? 'Processing...' : 'Review & Sign'}
          </Button>
          <Button 
            variant="secondary"
            className="w-full"
            onClick={handleCancel}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
        </div>
      </div>
    </div>
  );
};
