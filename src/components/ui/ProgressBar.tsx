

import React from 'react';
import { cn } from '@/lib/utils';

interface ProgressBarProps {
  current: number;
  total: number;
  className?: string;
  showPercentage?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  current,
  total,
  className = '',
  showPercentage = false
}) => {
  const percentage = Math.min((current / total) * 100, 100);

  return (
    <div className={cn('w-full', className)}>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div 
          className="bg-blue-500 h-2 rounded-full transition-all duration-300" 
          style={{ width: `${percentage}%` }}
        />
      </div>
      {showPercentage && (
        <div className="flex justify-between text-sm text-gray-600 mt-1">
          <span>{current.toLocaleString()}</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
    </div>
  );
};
