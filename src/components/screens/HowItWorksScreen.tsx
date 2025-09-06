'use client'

import React, { useState, useEffect } from 'react';
import { ArrowLeft, CheckCircle, Lock, Users, DollarSign, Shield, Clock } from 'lucide-react';
import { Button } from '@/components/ui';
import { useApp } from '@/lib/context';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ogc';
  timestamp: string;
  isTyping?: boolean;
  name?: string;
  avatar?: string;
}

export const HowItWorksScreen: React.FC = () => {
  const { setCurrentScreen } = useApp();
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [isTyping, setIsTyping] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const conversationFlow: Omit<Message, 'id' | 'timestamp'>[] = [
    {
      text: "Hey! I heard about OGC but I'm not sure how it works. Can you explain it to me?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Absolutely! OGC is a smart contract platform that makes group travel funding super easy and secure. Let me break it down for you! 🚀",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "So how does the funding work exactly?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Great question! Here's the magic: You connect your crypto wallet (like Algorand) and set up automatic payments. OGC handles the rest!",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "Wait, so my money stays in MY wallet?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Exactly! 💯 Your funds never leave your wallet until the trip is fully funded. You maintain complete control and ownership.",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "That's actually really cool! But what if I want to back out of a trip?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Good question! There are two ways to exit: 1) 75% of the group agrees to end funding, or 2) Your trip mates agree to release you. It's democratic and fair!",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "What about the payments? How often do I pay?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "You choose! Weekly, bi-weekly, or monthly contributions. OGC calculates the perfect amount based on your trip cost and timeline. No guesswork!",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "This sounds amazing! What makes it different from just using a regular savings account?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Great question! Unlike a savings account, OGC uses smart contracts for:\n\n• Automatic payments\n• Group consensus\n• Transparent tracking\n• Lower fees\n• Global accessibility\n• No bank restrictions",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "What about security? Is my money safe?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Security is our top priority! 🔒 Your funds are protected by:\n\n• Smart contracts (tamper-proof)\n• Multi-signature requirements\n• Your wallet stays in your control\n• Transparent, auditable code\n• No central authority can access your funds",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    },
    {
      text: "I'm sold! How do I get started?",
      sender: 'user',
      name: 'Sarah',
      avatar: '👩‍💼'
    },
    {
      text: "Perfect! Just connect your wallet, create or join a trip, and you're all set! Ready to start your first adventure? 🌍✈️",
      sender: 'ogc',
      name: 'OGC Support',
      avatar: '🤖'
    }
  ];

  useEffect(() => {
    const timer = setTimeout(() => {
      if (currentMessageIndex < conversationFlow.length) {
        const message = conversationFlow[currentMessageIndex];
        
        if (message.sender === 'ogc') {
          setIsTyping(true);
          
          setTimeout(() => {
            setMessages(prev => [...prev, {
              id: Date.now(),
              text: message.text,
              sender: message.sender,
              timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
              name: message.name,
              avatar: message.avatar
            }]);
            setIsTyping(false);
            setCurrentMessageIndex(prev => prev + 1);
          }, 800); // Faster typing
        } else {
          setMessages(prev => [...prev, {
            id: Date.now(),
            text: message.text,
            sender: message.sender,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            name: message.name,
            avatar: message.avatar
          }]);
          setCurrentMessageIndex(prev => prev + 1);
        }
      } else {
        setIsComplete(true);
      }
    }, currentMessageIndex === 0 ? 500 : 1000); // Faster message timing

    return () => clearTimeout(timer);
  }, [currentMessageIndex]);

  const skipToEnd = () => {
    setMessages(conversationFlow.map((msg, index) => ({
      id: Date.now() + index,
      text: msg.text,
      sender: msg.sender,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      name: msg.name,
      avatar: msg.avatar
    })));
    setCurrentMessageIndex(conversationFlow.length);
    setIsComplete(true);
    setIsTyping(false);
  };

  const handleGetStarted = () => {
    setCurrentScreen('connect-wallet');
  };

  const handleBack = () => {
    setCurrentScreen('splash');
  };

  return (
    <div className="min-h-screen bg-gray-100 lg:bg-white" style={{ fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}>
      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn {
          animation: fadeIn 0.3s ease-out forwards;
        }
        .message-bubble {
          max-width: 280px;
          word-wrap: break-word;
        }
        .message-bubble.user {
          background: #007AFF;
          color: white;
          border-radius: 18px 18px 4px 18px;
        }
        .message-bubble.ogc {
          background: #E5E5EA;
          color: #000;
          border-radius: 18px 18px 18px 4px;
        }
        .typing-dots {
          display: inline-block;
          width: 4px;
          height: 4px;
          border-radius: 50%;
          background-color: #999;
          animation: typing 1.4s infinite ease-in-out;
        }
        .typing-dots:nth-child(1) { animation-delay: -0.32s; }
        .typing-dots:nth-child(2) { animation-delay: -0.16s; }
        @keyframes typing {
          0%, 80%, 100% { transform: scale(0); }
          40% { transform: scale(1); }
        }
        .status-bar {
          background: linear-gradient(180deg, #000 0%, #1a1a1a 100%);
          color: white;
          font-size: 14px;
          font-weight: 600;
        }
      `}</style>
      
      {/* iPhone Status Bar */}
      <div className="status-bar px-4 py-1 flex justify-between items-center text-xs">
        <div className="flex items-center gap-1">
          <span>9:41</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
            <div className="w-1 h-1 bg-white rounded-full"></div>
          </div>
          <span>100%</span>
        </div>
      </div>
      
      {/* iPhone-style Header */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 sticky top-0 z-10" style={{ background: 'linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%)' }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={handleBack} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <ArrowLeft className="w-5 h-5 text-blue-500" />
            </button>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center shadow-sm">
                <span className="text-white font-bold text-lg">🤖</span>
              </div>
              <div>
                <h1 className="font-semibold text-gray-900 text-base">OGC Support</h1>
                <p className="text-xs text-green-500 font-medium">● Online</p>
              </div>
            </div>
          </div>
          {!isComplete && (
            <button
              onClick={skipToEnd}
              className="text-sm text-blue-500 hover:text-blue-700 font-medium px-3 py-1 rounded-full hover:bg-blue-50 transition-colors"
            >
              Skip
            </button>
          )}
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-1 lg:max-w-4xl lg:mx-auto" style={{ background: 'linear-gradient(180deg, #f0f0f0 0%, #e5e5ea 100%)' }}>
        {messages.map((message, index) => {
          const prevMessage = index > 0 ? messages[index - 1] : null;
          const showAvatar = !prevMessage || prevMessage.sender !== message.sender;
          const isGrouped = prevMessage && prevMessage.sender === message.sender;
          
          return (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-1 animate-fadeIn`}
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div className={`flex items-end gap-2 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar - only show if not grouped */}
                {showAvatar && (
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm mb-1 ${
                    message.sender === 'user' 
                      ? 'bg-gradient-to-br from-pink-400 to-pink-500' 
                      : 'bg-gradient-to-br from-blue-500 to-blue-600'
                  }`}>
                    {message.avatar}
                  </div>
                )}
                
                {/* Spacer for grouped messages */}
                {isGrouped && <div className="w-8"></div>}
                
                {/* Message Bubble */}
                <div className={`message-bubble ${message.sender} px-4 py-2 shadow-sm ${isGrouped ? 'mt-0' : ''}`}>
                  <p className="text-sm leading-relaxed whitespace-pre-line" style={{ lineHeight: '1.4' }}>
                    {message.text}
                  </p>
                  <p className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                  }`} style={{ fontSize: '11px' }}>
                    {message.timestamp}
                  </p>
                </div>
              </div>
            </div>
          );
        })}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex justify-start mb-1">
            <div className="flex items-end gap-2">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-sm mb-1">
                🤖
              </div>
              <div className="message-bubble ogc px-4 py-2 shadow-sm">
                <div className="flex items-center gap-1">
                  <span className="typing-dots"></span>
                  <span className="typing-dots"></span>
                  <span className="typing-dots"></span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* iPhone-style Bottom Section */}
      {isComplete && (
        <div className="bg-white border-t border-gray-200 p-4" style={{ background: 'linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%)' }}>
          <div className="space-y-4">
            <div className="text-center">
              <h3 className="font-semibold text-gray-900 text-lg mb-2">Ready to get started?</h3>
              <p className="text-sm text-gray-600">Join thousands of travelers using OGC</p>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center gap-2 p-3 bg-green-50 rounded-2xl border border-green-100">
                <Shield className="w-5 h-5 text-green-600" />
                <span className="text-sm font-medium text-green-800">Secure</span>
              </div>
              <div className="flex items-center gap-2 p-3 bg-blue-50 rounded-2xl border border-blue-100">
                <Clock className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-800">Automatic</span>
              </div>
              <div className="flex items-center gap-2 p-3 bg-purple-50 rounded-2xl border border-purple-100">
                <Users className="w-5 h-5 text-purple-600" />
                <span className="text-sm font-medium text-purple-800">Democratic</span>
              </div>
              <div className="flex items-center gap-2 p-3 bg-orange-50 rounded-2xl border border-orange-100">
                <DollarSign className="w-5 h-5 text-orange-600" />
                <span className="text-sm font-medium text-orange-800">Low Fees</span>
              </div>
            </div>
            
            <Button 
              onClick={handleGetStarted}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-4 rounded-2xl shadow-lg transition-all duration-200 transform hover:scale-105"
              size="lg"
            >
              Get Started with OGC
            </Button>
            
            <p className="text-xs text-gray-500 text-center">
              Free to use • No hidden fees • Your funds stay secure
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
