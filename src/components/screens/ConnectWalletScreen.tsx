'use client'
import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';
import { mockWallets } from '@/lib/mockData';

export const ConnectWalletScreen: React.FC = () => {
  const { setCurrentScreen, setWalletConnected, setUser } = useApp();

  const handleWalletConnect = (_walletName: string) => {
    // Simulate wallet connection
    setWalletConnected(true);
    setUser({
      id: '1',
      name: 'Alice',
      walletAddress: '0x1234...5678',
      avatar: 'A'
    });
    setCurrentScreen('trip-list');
  };

  const handleDemoMode = () => {
    setCurrentScreen('trip-list');
  };

  return (
    <div className="min-h-screen bg-white p-6">
      <div className="max-w-sm mx-auto pt-12">
        <h1 className="text-2xl font-bold text-black mb-8">Connect your Algorand wallet</h1>
        
        <div className="space-y-4 mb-8">
          {mockWallets.map((wallet, index) => (
            <div 
              key={index}
              onClick={() => handleWalletConnect(wallet.name)}
              className="p-4 border border-gray-200 rounded-xl flex items-center justify-between hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold ${
                  wallet.name === 'Pera Wallet' ? 'bg-blue-500' : 'bg-purple-500'
                }`}>
                  {wallet.icon}
                </div>
                <span className="font-medium">{wallet.name}</span>
              </div>
              <ArrowRight className="w-5 h-5 text-gray-400" />
            </div>
          ))}
        </div>

        <div className="space-y-3 mb-8">
          <ChatBubble message="Your funds stay in your wallet." sender="left" />
          <ChatBubble message="Weekly contributions are signed by you." sender="right" />
        </div>

        <div className="space-y-4">
          <Button 
            onClick={() => handleWalletConnect('WalletConnect')}
            className="w-full"
          >
            Connect with WalletConnect
          </Button>
          <Button 
            variant="secondary"
            onClick={handleDemoMode}
            className="w-full"
          >
            Continue without wallet (Demo mode)
          </Button>
        </div>

        <p className="text-xs text-gray-500 text-center mt-6">
          Algorand • USDC ASA • Low fees
        </p>
      </div>
    </div>
  );
};
