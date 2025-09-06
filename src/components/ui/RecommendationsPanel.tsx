import React, { useState, useEffect } from 'react';
import { Plane, Hotel, Car, MapPin, Star, Clock, Users, Wifi, Waves, Utensils, Camera, Heart, ChevronRight, Loader2, Check } from 'lucide-react';
import { Button } from './Button';
import { travelApi, FlightOption, HotelOption, CarRentalOption, ExcursionOption } from '@/lib/api/travelApi';
import { useApp } from '@/lib/context';

interface RecommendationsPanelProps {
  destination: string;
  departureCity: string;
  startDate: string;
  endDate: string;
  groupSize: number;
  tripId?: number;
  className?: string;
  onSelectionChange?: (type: 'flights' | 'hotels' | 'cars' | 'activities', selections: any[]) => void;
}

type TabType = 'flights' | 'hotels' | 'cars' | 'excursions';

export const RecommendationsPanel: React.FC<RecommendationsPanelProps> = ({
  destination,
  departureCity,
  startDate,
  endDate,
  groupSize,
  tripId,
  className = '',
  onSelectionChange
}) => {
  const [activeTab, setActiveTab] = useState<TabType>('flights');
  const [loading, setLoading] = useState(false);
  const [flights, setFlights] = useState<FlightOption[]>([]);
  const [hotels, setHotels] = useState<HotelOption[]>([]);
  const [cars, setCarRentals] = useState<CarRentalOption[]>([]);
  const [excursions, setExcursions] = useState<ExcursionOption[]>([]);
  
  // Selection state
  const [selectedFlights, setSelectedFlights] = useState<FlightOption[]>([]);
  const [selectedHotels, setSelectedHotels] = useState<HotelOption[]>([]);
  const [selectedCars, setSelectedCars] = useState<CarRentalOption[]>([]);
  const [selectedActivities, setSelectedActivities] = useState<ExcursionOption[]>([]);

  const tabs = [
    { id: 'flights' as TabType, label: 'Flights', icon: Plane, count: flights.length },
    { id: 'hotels' as TabType, label: 'Hotels', icon: Hotel, count: hotels.length },
    { id: 'cars' as TabType, label: 'Cars', icon: Car, count: cars.length },
    { id: 'excursions' as TabType, label: 'Activities', icon: MapPin, count: excursions.length }
  ];

  const loadRecommendations = async (tab: TabType) => {
    if (loading) return;
    
    setLoading(true);
    try {
      switch (tab) {
        case 'flights':
          if (flights.length === 0) {
            const flightData = await travelApi.searchFlights(departureCity, destination, startDate, endDate, groupSize);
            setFlights(flightData);
          }
          break;
        case 'hotels':
          if (hotels.length === 0) {
            const hotelData = await travelApi.searchHotels(destination, startDate, endDate, groupSize, Math.ceil(groupSize / 2));
            setHotels(hotelData);
          }
          break;
        case 'cars':
          if (cars.length === 0) {
            const carData = await travelApi.searchCarRentals(destination, startDate, endDate);
            setCarRentals(carData);
          }
          break;
        case 'excursions':
          if (excursions.length === 0) {
            const excursionData = await travelApi.searchExcursions(destination, startDate, endDate);
            setExcursions(excursionData);
          }
          break;
      }
    } catch (error) {
      console.error(`Error loading ${tab}:`, error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecommendations(activeTab);
  }, [activeTab, destination, departureCity, startDate, endDate, groupSize]);

  const formatPrice = (price: number, currency: string = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(price);
  };

  // Selection handlers
  const handleSelectItem = (type: 'flights' | 'hotels' | 'cars' | 'activities', item: any) => {
    switch (type) {
      case 'flights':
        const newFlights = selectedFlights.find(f => f.id === item.id) 
          ? selectedFlights.filter(f => f.id !== item.id)
          : [...selectedFlights, item];
        setSelectedFlights(newFlights);
        onSelectionChange?.('flights', newFlights);
        break;
      case 'hotels':
        const newHotels = selectedHotels.find(h => h.id === item.id)
          ? selectedHotels.filter(h => h.id !== item.id)
          : [...selectedHotels, item];
        setSelectedHotels(newHotels);
        onSelectionChange?.('hotels', newHotels);
        break;
      case 'cars':
        const newCars = selectedCars.find(c => c.id === item.id)
          ? selectedCars.filter(c => c.id !== item.id)
          : [...selectedCars, item];
        setSelectedCars(newCars);
        onSelectionChange?.('cars', newCars);
        break;
      case 'activities':
        const newActivities = selectedActivities.find(a => a.id === item.id)
          ? selectedActivities.filter(a => a.id !== item.id)
          : [...selectedActivities, item];
        setSelectedActivities(newActivities);
        onSelectionChange?.('activities', newActivities);
        break;
    }
  };

  const isSelected = (type: 'flights' | 'hotels' | 'cars' | 'activities', itemId: string) => {
    switch (type) {
      case 'flights':
        return selectedFlights.some(f => f.id === itemId);
      case 'hotels':
        return selectedHotels.some(h => h.id === itemId);
      case 'cars':
        return selectedCars.some(c => c.id === itemId);
      case 'activities':
        return selectedActivities.some(a => a.id === itemId);
      default:
        return false;
    }
  };

  const renderFlights = () => (
    <div className="space-y-4">
      {flights.map((flight) => {
        const selected = isSelected('flights', flight.id);
        return (
        <div key={flight.id} className={`p-4 border rounded-2xl hover:bg-gray-50 transition-colors ${
          selected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
        }`}>
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Plane className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{flight.airline}</h3>
                <p className="text-sm text-gray-600">{flight.flightNumber} • {flight.aircraft}</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xl font-bold text-blue-600">{formatPrice(flight.price)}</p>
              <p className="text-xs text-gray-500">per person</p>
            </div>
          </div>
          
          <div className="flex items-center justify-between mb-3">
            <div className="text-center">
              <p className="text-sm font-medium text-gray-900">{flight.departure.time}</p>
              <p className="text-xs text-gray-500">{flight.departure.airport}</p>
              <p className="text-xs text-gray-500">{flight.departure.city}</p>
            </div>
            <div className="flex-1 mx-4">
              <div className="flex items-center justify-center">
                <div className="flex-1 h-px bg-gray-300"></div>
                <div className="px-2 text-xs text-gray-500">{flight.duration}</div>
                <div className="flex-1 h-px bg-gray-300"></div>
              </div>
              <p className="text-center text-xs text-gray-500 mt-1">
                {flight.stops === 0 ? 'Direct' : `${flight.stops} stop${flight.stops > 1 ? 's' : ''}`}
              </p>
            </div>
            <div className="text-center">
              <p className="text-sm font-medium text-gray-900">{flight.arrival.time}</p>
              <p className="text-xs text-gray-500">{flight.arrival.airport}</p>
              <p className="text-xs text-gray-500">{flight.arrival.city}</p>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                {flight.class}
              </span>
              {flight.stops === 0 && (
                <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                  Direct
                </span>
              )}
            </div>
            <Button 
              size="sm" 
              className="px-4"
              onClick={() => handleSelectItem('flights', flight)}
              variant={selected ? 'secondary' : 'default'}
            >
              {selected ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Selected
                </>
              ) : (
                'Select Flight'
              )}
            </Button>
          </div>
        </div>
        );
      })}
    </div>
  );

  const renderHotels = () => (
    <div className="space-y-4">
      {hotels.map((hotel) => {
        const selected = isSelected('hotels', hotel.id);
        return (
        <div key={hotel.id} className={`p-4 border rounded-2xl hover:bg-gray-50 transition-colors ${
          selected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
        }`}>
          <div className="flex gap-4">
            <div className="w-24 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
              <img 
                src={hotel.images[0]} 
                alt={hotel.name}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900 truncate">{hotel.name}</h3>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <Star 
                          key={i} 
                          className={`w-4 h-4 ${i < hotel.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-500">{hotel.rating} stars</span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-blue-600">{formatPrice(hotel.price)}</p>
                  <p className="text-xs text-gray-500">per night</p>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-2">{hotel.location.address}, {hotel.location.city}</p>
              
              <div className="flex flex-wrap gap-1 mb-3">
                {hotel.amenities.slice(0, 4).map((amenity, index) => (
                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    {amenity}
                  </span>
                ))}
                {hotel.amenities.length > 4 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    +{hotel.amenities.length - 4} more
                  </span>
                )}
              </div>
              
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-500">
                  {hotel.rooms} room{hotel.rooms > 1 ? 's' : ''} • {hotel.guests} guest{hotel.guests > 1 ? 's' : ''}
                </div>
                <Button 
                  size="sm" 
                  className="px-4"
                  onClick={() => handleSelectItem('hotels', hotel)}
                  variant={selected ? 'secondary' : 'default'}
                >
                  {selected ? (
                    <>
                      <Check className="w-4 h-4 mr-2" />
                      Selected
                    </>
                  ) : (
                    'Select Hotel'
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
        );
      })}
    </div>
  );

  const renderCars = () => (
    <div className="space-y-4">
      {cars.map((car) => {
        const selected = isSelected('cars', car.id);
        return (
        <div key={car.id} className={`p-4 border rounded-2xl hover:bg-gray-50 transition-colors ${
          selected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
        }`}>
          <div className="flex gap-4">
            <div className="w-24 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
              <img 
                src={car.image} 
                alt={`${car.vehicle.make} ${car.vehicle.model}`}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{car.vehicle.make} {car.vehicle.model}</h3>
                  <p className="text-sm text-gray-600">{car.company}</p>
                  <p className="text-sm text-gray-500">{car.vehicle.year} • {car.vehicle.type} • {car.vehicle.seats} seats</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-blue-600">{formatPrice(car.price)}</p>
                  <p className="text-xs text-gray-500">per day</p>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-1 mb-3">
                {car.features.slice(0, 4).map((feature, index) => (
                  <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    {feature}
                  </span>
                ))}
                {car.features.length > 4 && (
                  <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">
                    +{car.features.length - 4} more
                  </span>
                )}
              </div>
              
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-500">
                  {car.duration} • {car.vehicle.transmission} • {car.vehicle.fuel}
                </div>
                <Button 
                  size="sm" 
                  className="px-4"
                  onClick={() => handleSelectItem('cars', car)}
                  variant={selected ? 'secondary' : 'default'}
                >
                  {selected ? (
                    <>
                      <Check className="w-4 h-4 mr-2" />
                      Selected
                    </>
                  ) : (
                    'Select Car'
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
        );
      })}
    </div>
  );

  const renderExcursions = () => (
    <div className="space-y-4">
      {excursions.map((excursion) => {
        const selected = isSelected('activities', excursion.id);
        return (
        <div key={excursion.id} className={`p-4 border rounded-2xl hover:bg-gray-50 transition-colors ${
          selected ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
        }`}>
          <div className="flex gap-4">
            <div className="w-24 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
              <img 
                src={excursion.images[0]} 
                alt={excursion.title}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{excursion.title}</h3>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-1">
                      {[...Array(5)].map((_, i) => (
                        <Star 
                          key={i} 
                          className={`w-4 h-4 ${i < excursion.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-500">{excursion.rating} ({excursion.reviews} reviews)</span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-blue-600">{formatPrice(excursion.price)}</p>
                  <p className="text-xs text-gray-500">per person</p>
                </div>
              </div>
              
              <p className="text-sm text-gray-600 mb-2">{excursion.description}</p>
              
              <div className="flex items-center gap-4 mb-3 text-sm text-gray-500">
                <div className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {excursion.duration}
                </div>
                <div className="flex items-center gap-1">
                  <Users className="w-4 h-4" />
                  Max {excursion.maxGroupSize}
                </div>
                <div className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {excursion.location.name}
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                    {excursion.category}
                  </span>
                  <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                    {excursion.cancellationPolicy}
                  </span>
                </div>
                <Button 
                  size="sm" 
                  className="px-4"
                  onClick={() => handleSelectItem('activities', excursion)}
                  variant={selected ? 'secondary' : 'default'}
                >
                  {selected ? (
                    <>
                      <Check className="w-4 h-4 mr-2" />
                      Selected
                    </>
                  ) : (
                    'Select Activity'
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
        );
      })}
    </div>
  );

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-4" />
            <p className="text-gray-500">Loading {tabs.find(t => t.id === activeTab)?.label}...</p>
          </div>
        </div>
      );
    }

    switch (activeTab) {
      case 'flights':
        return renderFlights();
      case 'hotels':
        return renderHotels();
      case 'cars':
        return renderCars();
      case 'excursions':
        return renderExcursions();
      default:
        return null;
    }
  };

  return (
    <div className={`bg-white rounded-2xl border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Travel Recommendations</h2>
        <p className="text-sm text-gray-600">
          {destination} • {new Date(startDate).toLocaleDateString()} - {new Date(endDate).toLocaleDateString()} • {groupSize} people
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center gap-2 px-4 py-4 text-sm font-medium transition-colors ${
                activeTab === tab.id
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
              {tab.count > 0 && (
                <span className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded-full">
                  {tab.count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Content */}
      <div className="p-6">
        {renderContent()}
      </div>
    </div>
  );
};
