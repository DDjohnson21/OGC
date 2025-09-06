import React from 'react';
import { cn } from '../../utils';

interface ChatBubbleProps {
  message: string;
  sender: 'left' | 'right';
  bold?: boolean;
  show?: boolean;
  className?: string;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  sender,
  bold = false,
  show = true,
  className = ''
}) => {
  return (
    <div className={cn(
      'flex mb-3',
      sender === 'right' ? 'justify-end' : 'justify-start',
      show ? 'animate-fadeIn' : 'opacity-0',
      className
    )}>
      <div className={cn(
        'max-w-xs px-4 py-3 rounded-[20px]',
        sender === 'right' 
          ? 'bg-blue-500 text-white' 
          : 'bg-gray-200 text-black',
        bold ? 'font-bold' : '',
        className
      )}>
        {message}
      </div>
    </div>
  );
};
