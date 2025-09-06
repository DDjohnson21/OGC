'use client'

import React, { useState, useEffect } from 'react';
import { Plane, ArrowRight } from 'lucide-react';
import { Button, ChatBubble } from '@/components/ui';
import { useApp } from '@/lib/context';
import { onboardingMessages } from '@/lib/mockData';

export const SplashScreen: React.FC = () => {
  const { setCurrentScreen } = useApp();
  const [typingIndex, setTypingIndex] = useState(0);
  const [showAnimation, setShowAnimation] = useState(false);

  useEffect(() => {
    // Start typing animation after a short delay
    const timer = setTimeout(() => {
      setShowAnimation(true);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (showAnimation && typingIndex < onboardingMessages.length - 1) {
      const timer = setTimeout(() => {
        setTypingIndex(prev => prev + 1);
      }, onboardingMessages[typingIndex + 1]?.delay || 0);
      return () => clearTimeout(timer);
    }
  }, [showAnimation, typingIndex]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-sm">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="text-xs text-gray-500 mb-4">Get</div>
          <div className="flex items-center justify-center gap-3 mb-2">
            <div className="relative">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center">
                <Plane className="w-8 h-8 text-white" />
              </div>
              {showAnimation && typingIndex < onboardingMessages.length && (
                <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2">
                  <div className="flex space-x-1">
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-typing"></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-1 h-1 bg-gray-400 rounded-full animate-typing" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              )}
            </div>
            <h1 className="text-3xl font-bold text-black">OGC</h1>
          </div>
          <p className="text-gray-600 text-lg">Out The Group Chat</p>
          <p className="text-gray-500 text-sm mt-1">Contribute & Explore Together</p>
        </div>

        {/* Chat Messages */}
        <div className="mb-12 min-h-[200px]">
          {onboardingMessages.map((msg, index) => (
            <ChatBubble 
              key={index}
              message={msg.text} 
              sender={msg.sender} 
              bold={msg.bold}
              show={index <= typingIndex}
            />
          ))}
        </div>

        {/* Action Buttons */}
        <div className="space-y-4">
          <Button 
            onClick={() => setCurrentScreen('connect-wallet')}
            className="w-full flex items-center justify-center gap-2"
            size="lg"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </Button>
          <button 
            onClick={() => setCurrentScreen('how-it-works')}
            className="w-full text-blue-500 text-sm hover:underline"
          >
            Learn how it works
          </button>
        </div>
      </div>
    </div>
  );
};
