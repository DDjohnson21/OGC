import React, { useState } from 'react';
import { ArrowLeft, Plus, MapPin } from 'lucide-react';
import { Button, ChatBubble } from '../components/ui';
import { useApp } from '../context/AppContext';

interface ItineraryItem {
  id: number;
  day: string;
  activity: string;
  location: string;
  checked: boolean;
}

export const MapScreen: React.FC = () => {
  const { setCurrentScreen } = useApp();
  const [itinerary, setItinerary] = useState<ItineraryItem[]>([
    { id: 1, day: 'Day 1', activity: 'Rome Tour', location: 'Rome', checked: true },
    { id: 2, day: 'Day 2', activity: 'Vatican Museums', location: 'Vatican City', checked: false },
    { id: 3, day: 'Day 3', activity: 'Colosseum & Forum', location: 'Rome', checked: false },
    { id: 4, day: 'Day 4', activity: 'Travel to Milan', location: 'Milan', checked: false },
    { id: 5, day: 'Day 5', activity: 'Milan Cathedral', location: 'Milan', checked: false }
  ]);

  const toggleItem = (id: number) => {
    setItinerary(items => 
      items.map(item => 
        item.id === id ? { ...item, checked: !item.checked } : item
      )
    );
  };

  const addStop = () => {
    const newItem: ItineraryItem = {
      id: Date.now(),
      day: `Day ${itinerary.length + 1}`,
      activity: 'New Activity',
      location: 'New Location',
      checked: false
    };
    setItinerary([...itinerary, newItem]);
  };

  const mapPins = [
    { id: 1, location: 'Rome', x: 20, y: 30, color: 'bg-red-500' },
    { id: 2, location: 'Milan', x: 80, y: 20, color: 'bg-red-500' },
    { id: 3, location: 'Naples', x: 70, y: 80, color: 'bg-red-500' }
  ];

  return (
    <div className="min-h-screen bg-white p-6">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button onClick={() => setCurrentScreen('trip-detail')}>
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold ml-4">Itinerary</h1>
      </div>

      {/* Map View */}
      <div className="mb-6">
        <div className="w-full h-48 bg-gradient-to-r from-blue-400 to-green-400 rounded-xl relative overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center text-white">
            <p className="text-lg font-medium">Rome • Milan • Naples</p>
          </div>
          
          {/* Map Pins */}
          {mapPins.map(pin => (
            <div 
              key={pin.id}
              className={`absolute w-3 h-3 ${pin.color} rounded-full`}
              style={{ 
                left: `${pin.x}%`, 
                top: `${pin.y}%` 
              }}
            />
          ))}
          
          {/* Map Controls */}
          <div className="absolute top-4 right-4 flex gap-2">
            <button className="p-2 bg-white/20 rounded-full text-white hover:bg-white/30 transition-colors">
              <MapPin className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Info Message */}
      <div className="mb-4">
        <ChatBubble message="Add stops to share with the group." sender="left" />
      </div>

      {/* Itinerary Items */}
      <div className="space-y-3 mb-6">
        {itinerary.map((item) => (
          <div key={item.id} className="flex items-center gap-3 p-3 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
            <input 
              type="checkbox" 
              checked={item.checked}
              onChange={() => toggleItem(item.id)}
              className="rounded text-blue-500 focus:ring-blue-500"
            />
            <div className="flex-1">
              <p className="font-medium">{item.day}</p>
              <p className="text-sm text-gray-600">{item.activity}</p>
              <p className="text-xs text-gray-500">{item.location}</p>
            </div>
            <button 
              onClick={() => setItinerary(items => items.filter(i => i.id !== item.id))}
              className="text-gray-400 hover:text-red-500 transition-colors"
            >
              ×
            </button>
          </div>
        ))}
      </div>

      {/* Add Stop Button */}
      <Button 
        onClick={addStop}
        className="w-full"
        variant="outline"
      >
        <Plus className="w-4 h-4 mr-2" />
        Add Stop
      </Button>

      {/* Trip Stats */}
      <div className="mt-6 p-4 bg-gray-50 rounded-xl">
        <h3 className="font-semibold text-gray-900 mb-2">Trip Progress</h3>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-blue-600">
              {itinerary.filter(item => item.checked).length}
            </p>
            <p className="text-sm text-gray-600">Completed</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-600">
              {itinerary.length - itinerary.filter(item => item.checked).length}
            </p>
            <p className="text-sm text-gray-600">Remaining</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-600">
              {Math.round((itinerary.filter(item => item.checked).length / itinerary.length) * 100)}%
            </p>
            <p className="text-sm text-gray-600">Progress</p>
          </div>
        </div>
      </div>
    </div>
  );
};
