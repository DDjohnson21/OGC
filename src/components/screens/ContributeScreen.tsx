'use client'
import React, { useState } from 'react';
import { Button, Input, Select, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';
import { formatCurrency } from '@/lib/utils';

export const ContributeScreen: React.FC = () => {
  const { state, setCurrentScreen } = useApp();
  const { selectedTrip } = state;
  const [selectedAmount, setSelectedAmount] = useState(25);
  const [customAmount, setCustomAmount] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedWallet, setSelectedWallet] = useState('usdc');
  const [showSuccess, setShowSuccess] = useState(false);

  const handleContribute = async () => {
    setIsSubmitting(true);
    
    // Simulate transaction
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    setShowSuccess(true);
    
    // Show success message for 2 seconds then navigate
    setTimeout(() => {
      setCurrentScreen('trip-detail');
    }, 2000);
  };

  const handleCancel = () => {
    setCurrentScreen('trip-detail');
  };

  const amount = customAmount ? parseInt(customAmount) : selectedAmount;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-end z-50">
      <div className="w-full bg-white rounded-t-3xl p-6 max-h-[80vh] overflow-y-auto">
        <div className="w-12 h-1 bg-gray-300 rounded-full mx-auto mb-6" />
        
        <h2 className="text-xl font-bold mb-2">Contribute to {selectedTrip?.name}</h2>
        {selectedTrip?.contributionSchedule && (
          <p className="text-sm text-gray-600 mb-6">
            {selectedTrip.contributionSchedule.charAt(0).toUpperCase() + selectedTrip.contributionSchedule.slice(1)} contribution: {formatCurrency(selectedTrip.contributionAmount || 0)}
          </p>
        )}
        
        <ChatBubble 
          message={`💰 Choose your contribution amount. Your ${selectedTrip?.contributionSchedule} contribution is ${formatCurrency(selectedTrip?.contributionAmount || 0)} per person.`}
          sender="system" 
          type="tip"
          avatar="💰"
          name="OGC Assistant"
        />
        
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
          <Select
            options={[
              {
                value: 'usdc',
                label: 'USDC Wallet',
                description: 'Connected wallet with USDC',
                icon: '💰'
              },
              {
                value: 'bank',
                label: 'Bank Account',
                description: 'Coming Soon',
                icon: '🏦'
              }
            ]}
            value={selectedWallet}
            onChange={setSelectedWallet}
            placeholder="Select payment method"
          />
          
          {/* Network Fee Info */}
          <div className="p-3 bg-gray-50 rounded-xl">
            <p className="text-sm text-gray-600">Network fee: ~$0.001 ALGO</p>
            <p className="text-xs text-gray-500 mt-1">Total: {amount} USDC + 0.001 ALGO</p>
          </div>
        </div>
        
        {showSuccess ? (
          <ChatBubble 
            message={`✅ Contribution of ${formatCurrency(amount)} sent successfully! Your funds are now part of the trip pool.`}
            sender="system" 
            type="success"
            avatar="✅"
            name="OGC Assistant"
          />
        ) : (
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
        )}
      </div>
    </div>
  );
};
