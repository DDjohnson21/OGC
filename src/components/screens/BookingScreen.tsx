'use client'
import React, { useState } from 'react';
import { ArrowLeft, Plane, MapPin, Download } from 'lucide-react';
import { Button, Chip } from '@/components/ui';
import { useApp } from '@/lib/context';
import { formatCurrency } from '@/lib/utils';

export const BookingScreen: React.FC = () => {
  const { setCurrentScreen } = useApp();
  const [isApproved] = useState(true); // Simulate approved state

  const bookingDetails = {
    flight: {
      route: 'BOS → FCO',
      dates: 'Mar 15-22, 2025',
      airline: 'Emirates',
      price: 1200
    },
    hotel: {
      nights: 3,
      location: 'Rome Center',
      price: 450
    },
    total: 1650
  };

  const handlePayment = () => {
    if (isApproved) {
      alert('Payment processed! Itinerary downloaded. ✈️');
    } else {
      alert('This action requires 75% member approval.');
    }
  };

  return (
    <div className="min-h-screen bg-white p-6">
      {/* Header */}
      <div className="flex items-center mb-6">
        <button onClick={() => setCurrentScreen('trip-detail')}>
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h1 className="text-xl font-bold ml-4">Booking Confirmation</h1>
      </div>

      {/* Booking Details */}
      <div className="space-y-4 mb-6">
        {/* Flight Card */}
        <div className="p-4 border border-gray-200 rounded-xl">
          <div className="flex items-center gap-3 mb-2">
            <Plane className="w-5 h-5 text-blue-500" />
            <span className="font-medium">Flight</span>
          </div>
          <p className="text-sm text-gray-600">{bookingDetails.flight.route}</p>
          <p className="text-sm text-gray-600">{bookingDetails.flight.dates} • {bookingDetails.flight.airline}</p>
          <p className="font-medium mt-2">{formatCurrency(bookingDetails.flight.price)}</p>
        </div>

        {/* Hotel Card */}
        <div className="p-4 border border-gray-200 rounded-xl">
          <div className="flex items-center gap-3 mb-2">
            <MapPin className="w-5 h-5 text-blue-500" />
            <span className="font-medium">Hotel</span>
          </div>
          <p className="text-sm text-gray-600">{bookingDetails.hotel.nights} nights • {bookingDetails.hotel.location}</p>
          <p className="font-medium mt-2">{formatCurrency(bookingDetails.hotel.price)}</p>
        </div>
      </div>

      {/* Total */}
      <div className="border-t pt-4 mb-6">
        <div className="flex justify-between items-center">
          <span className="text-lg font-bold">Total</span>
          <span className="text-lg font-bold">{formatCurrency(bookingDetails.total)}</span>
        </div>
      </div>

      {/* Payment Section */}
      <div className="space-y-4">
        <Button 
          className="w-full"
          onClick={handlePayment}
        >
          Pay from Trip Pool
        </Button>
        
        <div className="text-center">
          {!isApproved ? (
            <Chip>Requires 75% Approvals</Chip>
          ) : (
            <div className="p-4 bg-green-50 rounded-xl">
              <p className="text-green-800 font-medium">✅ Payment approved!</p>
              <Button 
                variant="secondary" 
                className="mt-2"
                onClick={() => alert('Itinerary downloaded! 📄')}
              >
                <Download className="w-4 h-4 mr-2" />
                Download Itinerary.pdf
              </Button>
            </div>
          )}
        </div>

        {/* Booking Summary */}
        <div className="mt-6 p-4 bg-blue-50 rounded-xl">
          <h3 className="font-semibold text-blue-900 mb-2">Booking Summary</h3>
          <div className="space-y-1 text-sm text-blue-800">
            <p>• Confirmation: #EMR-789456</p>
            <p>• Check-in: March 15, 2025</p>
            <p>• Check-out: March 18, 2025</p>
            <p>• Flight: EK123 (BOS→FCO)</p>
          </div>
        </div>
      </div>
    </div>
  );
};
