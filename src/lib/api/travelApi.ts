// Travel API service for real-time recommendations
// Using free APIs for demo purposes
// In production, replace mock data with real API calls

import { API_CONFIG, getApiHeaders } from './config';

export interface FlightOption {
  id: string;
  airline: string;
  flightNumber: string;
  departure: {
    airport: string;
    city: string;
    time: string;
    date: string;
  };
  arrival: {
    airport: string;
    city: string;
    time: string;
    date: string;
  };
  duration: string;
  price: number;
  currency: string;
  stops: number;
  aircraft: string;
  class: string;
}

export interface HotelOption {
  id: string;
  name: string;
  rating: number;
  price: number;
  currency: string;
  location: {
    address: string;
    city: string;
    coordinates: {
      lat: number;
      lng: number;
    };
  };
  amenities: string[];
  images: string[];
  checkIn: string;
  checkOut: string;
  rooms: number;
  guests: number;
}

export interface CarRentalOption {
  id: string;
  company: string;
  vehicle: {
    make: string;
    model: string;
    year: number;
    type: string;
    transmission: string;
    fuel: string;
    seats: number;
  };
  price: number;
  currency: string;
  duration: string;
  pickup: {
    location: string;
    address: string;
    time: string;
  };
  dropoff: {
    location: string;
    address: string;
    time: string;
  };
  features: string[];
  image: string;
}

export interface ExcursionOption {
  id: string;
  title: string;
  description: string;
  price: number;
  currency: string;
  duration: string;
  rating: number;
  reviews: number;
  category: string;
  location: {
    name: string;
    address: string;
    coordinates: {
      lat: number;
      lng: number;
    };
  };
  images: string[];
  includes: string[];
  excludes: string[];
  meetingPoint: string;
  languages: string[];
  maxGroupSize: number;
  cancellationPolicy: string;
}

// Mock data generators for demo (replace with real API calls)
export class TravelApiService {
  private static instance: TravelApiService;
  
  public static getInstance(): TravelApiService {
    if (!TravelApiService.instance) {
      TravelApiService.instance = new TravelApiService();
    }
    return TravelApiService.instance;
  }

  // Flight search using Amadeus API (free tier)
  async searchFlights(
    origin: string,
    destination: string,
    departureDate: string,
    returnDate?: string,
    passengers: number = 1
  ): Promise<FlightOption[]> {
    try {
      // Try real API first (uncomment when you have API keys)
      // return await this.searchFlightsAmadeus(origin, destination, departureDate, returnDate, passengers);
      
      // Fallback to mock data for demo
      return this.generateMockFlights(origin, destination, departureDate, returnDate, passengers);
    } catch (error) {
      console.error('Flight search error:', error);
      return this.generateMockFlights(origin, destination, departureDate, returnDate, passengers);
    }
  }

  // Real Amadeus API integration (uncomment when you have API keys)
  private async searchFlightsAmadeus(
    origin: string,
    destination: string,
    departureDate: string,
    returnDate?: string,
    passengers: number = 1
  ): Promise<FlightOption[]> {
    const amadeus = API_CONFIG.AMADEUS;
    const headers = getApiHeaders('AMADEUS');
    
    // First, get access token
    const tokenResponse = await fetch(`${amadeus.BASE_URL}/security/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: amadeus.API_KEY,
        client_secret: amadeus.API_SECRET
      })
    });
    
    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;
    
    // Search for flights
    const searchParams = new URLSearchParams({
      originLocationCode: this.getAirportCode(origin),
      destinationLocationCode: this.getAirportCode(destination),
      departureDate: departureDate,
      adults: passengers.toString(),
      max: '10'
    });
    
    if (returnDate) {
      searchParams.append('returnDate', returnDate);
    }
    
    const searchResponse = await fetch(
      `${amadeus.BASE_URL}${amadeus.ENDPOINTS.FLIGHTS}?${searchParams}`,
      {
        headers: {
          ...headers,
          'Authorization': `Bearer ${accessToken}`
        }
      }
    );
    
    const searchData = await searchResponse.json();
    
    // Transform Amadeus response to our format
    return searchData.data?.map((offer: any, index: number) => {
      const itinerary = offer.itineraries[0];
      const segments = itinerary.segments;
      const firstSegment = segments[0];
      const lastSegment = segments[segments.length - 1];
      
      return {
        id: `flight-${index + 1}`,
        airline: firstSegment.carrierCode,
        flightNumber: firstSegment.number,
        departure: {
          airport: firstSegment.departure.iataCode,
          city: firstSegment.departure.cityCode,
          time: new Date(firstSegment.departure.at).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          date: new Date(firstSegment.departure.at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        },
        arrival: {
          airport: lastSegment.arrival.iataCode,
          city: lastSegment.arrival.cityCode,
          time: new Date(lastSegment.arrival.at).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          date: new Date(lastSegment.arrival.at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        },
        duration: itinerary.duration,
        price: parseFloat(offer.price.total),
        currency: offer.price.currency,
        stops: segments.length - 1,
        aircraft: firstSegment.aircraft?.code || 'Unknown',
        class: offer.travelerPricings[0].fareDetailsBySegment[0].cabin || 'Economy'
      };
    }) || [];
  }

  // Hotel search using Booking.com API or similar
  async searchHotels(
    city: string,
    checkIn: string,
    checkOut: string,
    guests: number = 1,
    rooms: number = 1
  ): Promise<HotelOption[]> {
    try {
      // For demo, we'll use mock data
      // In production, replace with actual hotel API call
      return this.generateMockHotels(city, checkIn, checkOut, guests, rooms);
    } catch (error) {
      console.error('Hotel search error:', error);
      return this.generateMockHotels(city, checkIn, checkOut, guests, rooms);
    }
  }

  // Car rental search
  async searchCarRentals(
    city: string,
    pickupDate: string,
    dropoffDate: string,
    pickupTime: string = '10:00',
    dropoffTime: string = '10:00'
  ): Promise<CarRentalOption[]> {
    try {
      return this.generateMockCarRentals(city, pickupDate, dropoffDate, pickupTime, dropoffTime);
    } catch (error) {
      console.error('Car rental search error:', error);
      return this.generateMockCarRentals(city, pickupDate, dropoffDate, pickupTime, dropoffTime);
    }
  }

  // Excursions/Activities search
  async searchExcursions(
    city: string,
    startDate: string,
    endDate: string,
    category?: string
  ): Promise<ExcursionOption[]> {
    try {
      return this.generateMockExcursions(city, startDate, endDate, category);
    } catch (error) {
      console.error('Excursion search error:', error);
      return this.generateMockExcursions(city, startDate, endDate, category);
    }
  }

  // Mock data generators
  private generateMockFlights(
    origin: string,
    destination: string,
    departureDate: string,
    returnDate?: string,
    passengers: number = 1
  ): FlightOption[] {
    const airlines = ['American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue', 'Alaska Airlines'];
    const aircraft = ['Boeing 737', 'Airbus A320', 'Boeing 777', 'Airbus A350', 'Boeing 787'];
    const classes = ['Economy', 'Premium Economy', 'Business', 'First'];
    
    const flights: FlightOption[] = [];
    
    for (let i = 0; i < 5; i++) {
      const departureTime = new Date(departureDate);
      departureTime.setHours(6 + i * 3, Math.floor(Math.random() * 60));
      
      const arrivalTime = new Date(departureTime);
      arrivalTime.setHours(arrivalTime.getHours() + 2 + Math.floor(Math.random() * 8));
      
      flights.push({
        id: `flight-${i + 1}`,
        airline: airlines[Math.floor(Math.random() * airlines.length)],
        flightNumber: `${Math.floor(Math.random() * 9999) + 1000}`,
        departure: {
          airport: this.getAirportCode(origin),
          city: origin,
          time: departureTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          date: departureTime.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        },
        arrival: {
          airport: this.getAirportCode(destination),
          city: destination,
          time: arrivalTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          date: arrivalTime.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
        },
        duration: `${Math.floor(Math.random() * 8) + 2}h ${Math.floor(Math.random() * 60)}m`,
        price: Math.floor(Math.random() * 800) + 200,
        currency: 'USD',
        stops: Math.floor(Math.random() * 2),
        aircraft: aircraft[Math.floor(Math.random() * aircraft.length)],
        class: classes[Math.floor(Math.random() * classes.length)]
      });
    }
    
    return flights.sort((a, b) => a.price - b.price);
  }

  private generateMockHotels(
    city: string,
    checkIn: string,
    checkOut: string,
    guests: number,
    rooms: number
  ): HotelOption[] {
    const hotelNames = [
      'Grand Plaza Hotel', 'Marriott Downtown', 'Hilton Garden Inn', 'Holiday Inn Express',
      'Hyatt Regency', 'Sheraton Suites', 'Radisson Blu', 'InterContinental',
      'Four Seasons', 'Ritz-Carlton', 'Westin', 'DoubleTree'
    ];
    
    const amenities = [
      'Free WiFi', 'Pool', 'Gym', 'Spa', 'Restaurant', 'Bar', 'Room Service',
      'Concierge', 'Valet Parking', 'Business Center', 'Pet Friendly'
    ];
    
    const hotels: HotelOption[] = [];
    
    for (let i = 0; i < 6; i++) {
      const hotelAmenities = amenities.sort(() => 0.5 - Math.random()).slice(0, Math.floor(Math.random() * 6) + 3);
      
      hotels.push({
        id: `hotel-${i + 1}`,
        name: hotelNames[Math.floor(Math.random() * hotelNames.length)],
        rating: Math.floor(Math.random() * 2) + 4, // 4-5 stars
        price: Math.floor(Math.random() * 300) + 100,
        currency: 'USD',
        location: {
          address: `${Math.floor(Math.random() * 9999) + 100} Main St`,
          city: city,
          coordinates: {
            lat: 40.7128 + (Math.random() - 0.5) * 0.1,
            lng: -74.0060 + (Math.random() - 0.5) * 0.1
          }
        },
        amenities: hotelAmenities,
        images: [
          `https://picsum.photos/400/300?random=${i + 1}`,
          `https://picsum.photos/400/300?random=${i + 10}`,
          `https://picsum.photos/400/300?random=${i + 20}`
        ],
        checkIn: checkIn,
        checkOut: checkOut,
        rooms: rooms,
        guests: guests
      });
    }
    
    return hotels.sort((a, b) => a.price - b.price);
  }

  private generateMockCarRentals(
    city: string,
    pickupDate: string,
    dropoffDate: string,
    pickupTime: string,
    dropoffTime: string
  ): CarRentalOption[] {
    const companies = ['Hertz', 'Avis', 'Enterprise', 'Budget', 'Alamo', 'National'];
    const vehicles = [
      { make: 'Toyota', model: 'Camry', type: 'Sedan', seats: 5 },
      { make: 'Honda', model: 'Civic', type: 'Sedan', seats: 5 },
      { make: 'Ford', model: 'Explorer', type: 'SUV', seats: 7 },
      { make: 'Chevrolet', model: 'Malibu', type: 'Sedan', seats: 5 },
      { make: 'Nissan', model: 'Altima', type: 'Sedan', seats: 5 },
      { make: 'BMW', model: '3 Series', type: 'Luxury', seats: 5 }
    ];
    
    const features = [
      'Air Conditioning', 'GPS Navigation', 'Bluetooth', 'USB Ports',
      'Backup Camera', 'Cruise Control', 'Leather Seats', 'Sunroof'
    ];
    
    const carRentals: CarRentalOption[] = [];
    
    for (let i = 0; i < 4; i++) {
      const vehicle = vehicles[Math.floor(Math.random() * vehicles.length)];
      const vehicleFeatures = features.sort(() => 0.5 - Math.random()).slice(0, Math.floor(Math.random() * 4) + 3);
      
      carRentals.push({
        id: `car-${i + 1}`,
        company: companies[Math.floor(Math.random() * companies.length)],
        vehicle: {
          ...vehicle,
          year: 2022 + Math.floor(Math.random() * 2),
          transmission: Math.random() > 0.5 ? 'Automatic' : 'Manual',
          fuel: Math.random() > 0.5 ? 'Gasoline' : 'Hybrid'
        },
        price: Math.floor(Math.random() * 100) + 30,
        currency: 'USD',
        duration: this.calculateDuration(pickupDate, dropoffDate),
        pickup: {
          location: `${city} Airport`,
          address: `${city} International Airport`,
          time: pickupTime
        },
        dropoff: {
          location: `${city} Airport`,
          address: `${city} International Airport`,
          time: dropoffTime
        },
        features: vehicleFeatures,
        image: `https://picsum.photos/400/300?random=${i + 100}`
      });
    }
    
    return carRentals.sort((a, b) => a.price - b.price);
  }

  private generateMockExcursions(
    city: string,
    startDate: string,
    endDate: string,
    category?: string
  ): ExcursionOption[] {
    const excursions = [
      {
        title: 'City Walking Tour',
        description: 'Explore the historic downtown area with a knowledgeable local guide',
        category: 'Sightseeing',
        duration: '3 hours',
        price: 45,
        includes: ['Professional guide', 'Map', 'Water bottle'],
        excludes: ['Transportation', 'Meals', 'Tips'],
        languages: ['English', 'Spanish', 'French']
      },
      {
        title: 'Food & Wine Tasting',
        description: 'Sample local cuisine and wines at the best restaurants in the city',
        category: 'Food & Drink',
        duration: '4 hours',
        price: 85,
        includes: ['Food tastings', 'Wine pairings', 'Restaurant visits'],
        excludes: ['Transportation', 'Additional drinks', 'Tips'],
        languages: ['English', 'Italian']
      },
      {
        title: 'Adventure Hiking',
        description: 'Hike through scenic trails and enjoy breathtaking views',
        category: 'Adventure',
        duration: '6 hours',
        price: 65,
        includes: ['Hiking guide', 'Equipment', 'Lunch', 'Transportation'],
        excludes: ['Personal items', 'Tips'],
        languages: ['English', 'German']
      },
      {
        title: 'Museum & Art Gallery Tour',
        description: 'Visit world-class museums and art galleries with expert commentary',
        category: 'Culture',
        duration: '5 hours',
        price: 55,
        includes: ['Museum tickets', 'Expert guide', 'Audio guide'],
        excludes: ['Transportation', 'Meals', 'Tips'],
        languages: ['English', 'French', 'Spanish']
      },
      {
        title: 'Boat Cruise',
        description: 'Enjoy a relaxing boat cruise with stunning city views',
        category: 'Sightseeing',
        duration: '2 hours',
        price: 35,
        includes: ['Boat ticket', 'Commentary', 'Refreshments'],
        excludes: ['Meals', 'Tips'],
        languages: ['English', 'Spanish']
      },
      {
        title: 'Photography Workshop',
        description: 'Learn photography techniques while exploring the city',
        category: 'Education',
        duration: '4 hours',
        price: 75,
        includes: ['Professional photographer', 'Equipment rental', 'Photo editing tips'],
        excludes: ['Camera', 'Transportation', 'Tips'],
        languages: ['English']
      }
    ];
    
    const filteredExcursions = category 
      ? excursions.filter(ex => ex.category === category)
      : excursions;
    
    return filteredExcursions.map((excursion, index) => ({
      id: `excursion-${index + 1}`,
      ...excursion,
      currency: 'USD',
      rating: Math.floor(Math.random() * 1.5) + 4, // 4-5 stars
      reviews: Math.floor(Math.random() * 200) + 50,
      location: {
        name: `${city} City Center`,
        address: `${city} Downtown`,
        coordinates: {
          lat: 40.7128 + (Math.random() - 0.5) * 0.1,
          lng: -74.0060 + (Math.random() - 0.5) * 0.1
        }
      },
      images: [
        `https://picsum.photos/400/300?random=${index + 200}`,
        `https://picsum.photos/400/300?random=${index + 210}`,
        `https://picsum.photos/400/300?random=${index + 220}`
      ],
      meetingPoint: `${city} Tourist Information Center`,
      maxGroupSize: Math.floor(Math.random() * 15) + 10,
      cancellationPolicy: 'Free cancellation up to 24 hours before'
    }));
  }

  private getAirportCode(city: string): string {
    const airportCodes: { [key: string]: string } = {
      'New York': 'JFK',
      'Los Angeles': 'LAX',
      'Chicago': 'ORD',
      'Miami': 'MIA',
      'Boston': 'BOS',
      'Seattle': 'SEA',
      'Atlanta': 'ATL',
      'Denver': 'DEN',
      'Italy': 'FCO',
      'Japan': 'NRT',
      'Thailand': 'BKK',
      'France': 'CDG',
      'Spain': 'MAD',
      'Greece': 'ATH'
    };
    return airportCodes[city] || 'XXX';
  }

  private calculateDuration(startDate: string, endDate: string): string {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end.getTime() - start.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return `${diffDays} days`;
  }
}

// Export singleton instance
export const travelApi = TravelApiService.getInstance();
