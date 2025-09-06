import React from 'react';
import { cn } from '@/lib/utils';

interface ChatBubbleProps {
  message: string;
  sender: 'left' | 'right' | 'system';
  bold?: boolean;
  show?: boolean;
  className?: string;
  timestamp?: string;
  avatar?: string;
  name?: string;
  type?: 'info' | 'success' | 'warning' | 'error' | 'tip';
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  sender,
  bold = false,
  show = true,
  className = '',
  timestamp,
  avatar,
  name,
  type = 'info'
}) => {
  const getBubbleStyles = () => {
    if (sender === 'system') {
      switch (type) {
        case 'success':
          return 'bg-green-100 text-green-800 border border-green-200';
        case 'warning':
          return 'bg-yellow-100 text-yellow-800 border border-yellow-200';
        case 'error':
          return 'bg-red-100 text-red-800 border border-red-200';
        case 'tip':
          return 'bg-blue-50 text-blue-800 border border-blue-200';
        default:
          return 'bg-gray-100 text-gray-800 border border-gray-200';
      }
    }
    
    if (sender === 'right') {
      return 'bg-blue-500 text-white';
    }
    
    return 'bg-gray-200 text-black';
  };

  const getBubbleShape = () => {
    if (sender === 'system') {
      return 'rounded-2xl';
    }
    
    if (sender === 'right') {
      return 'rounded-[20px] rounded-br-[4px]';
    }
    
    return 'rounded-[20px] rounded-bl-[4px]';
  };

  return (
    <div className={cn(
      'flex mb-3',
      sender === 'right' ? 'justify-end' : 'justify-start',
      show ? 'animate-fadeIn' : 'opacity-0',
      className
    )}>
      <div className={cn(
        'max-w-xs sm:max-w-sm lg:max-w-md px-4 py-3 relative',
        getBubbleShape(),
        getBubbleStyles(),
        bold ? 'font-semibold' : 'font-normal',
        'shadow-sm'
      )}>
        {sender === 'system' && (
          <div className="flex items-center gap-2 mb-1">
            {avatar && (
              <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
                {avatar}
              </div>
            )}
            {name && (
              <span className="text-xs font-medium opacity-75">{name}</span>
            )}
          </div>
        )}
        
        <div className="text-sm leading-relaxed">
          {message}
        </div>
        
        {timestamp && (
          <div className={cn(
            'text-xs mt-1 opacity-60',
            sender === 'right' ? 'text-blue-100' : 'text-gray-500'
          )}>
            {timestamp}
          </div>
        )}
      </div>
    </div>
  );
};
