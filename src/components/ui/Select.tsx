import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SelectOption {
  value: string;
  label: string;
  description?: string;
  price?: string;
  icon?: string;
}

interface SelectProps {
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
  showPrice?: boolean;
}

export const Select: React.FC<SelectProps> = ({
  options,
  value,
  onChange,
  placeholder = "Select an option",
  className = "",
  disabled = false,
  showPrice = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedOption = options.find(option => option.value === value);

  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
    option.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (option: SelectOption) => {
    onChange(option.value);
    setIsOpen(false);
    setSearchTerm('');
  };

  return (
    <div className={cn("relative", className)} ref={dropdownRef}>
      <button
        type="button"
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        className={cn(
          "w-full px-4 py-4 text-left bg-white border border-gray-200 rounded-2xl",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
          "transition-all duration-200",
          "flex items-center justify-between",
          disabled ? "opacity-50 cursor-not-allowed" : "hover:border-gray-300",
          isOpen && "border-blue-500 ring-2 ring-blue-500"
        )}
      >
        <div className="flex-1 min-w-0">
          {selectedOption ? (
            <div className="flex items-center gap-3">
              {selectedOption.icon && (
                <span className="text-lg">{selectedOption.icon}</span>
              )}
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">
                  {selectedOption.label}
                </p>
                {selectedOption.description && (
                  <p className="text-sm text-gray-500 truncate">
                    {selectedOption.description}
                  </p>
                )}
              </div>
              {showPrice && selectedOption.price && (
                <p className="text-sm font-medium text-blue-600">
                  {selectedOption.price}
                </p>
              )}
            </div>
          ) : (
            <p className="text-gray-500">{placeholder}</p>
          )}
        </div>
        <ChevronDown 
          className={cn(
            "w-5 h-5 text-gray-400 transition-transform duration-200",
            isOpen && "rotate-180"
          )}
        />
      </button>

      {isOpen && (
        <div className="absolute z-50 w-full mt-2 bg-white border border-gray-200 rounded-2xl shadow-lg max-h-80 overflow-hidden">
          <div className="p-3 border-b border-gray-100">
            <input
              ref={inputRef}
              type="text"
              placeholder="Search..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />
          </div>
          <div className="max-h-60 overflow-y-auto">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => handleSelect(option)}
                  className={cn(
                    "w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors",
                    "flex items-center justify-between",
                    value === option.value && "bg-blue-50"
                  )}
                >
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    {option.icon && (
                      <span className="text-lg">{option.icon}</span>
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-gray-900 truncate">
                        {option.label}
                      </p>
                      {option.description && (
                        <p className="text-sm text-gray-500 truncate">
                          {option.description}
                        </p>
                      )}
                    </div>
                    {showPrice && option.price && (
                      <p className="text-sm font-medium text-blue-600">
                        {option.price}
                      </p>
                    )}
                  </div>
                  {value === option.value && (
                    <Check className="w-5 h-5 text-blue-600" />
                  )}
                </button>
              ))
            ) : (
              <div className="px-4 py-3 text-sm text-gray-500 text-center">
                No options found
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
