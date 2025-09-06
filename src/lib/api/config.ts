// API Configuration for Travel Services
// In production, these should be stored in environment variables

export const API_CONFIG = {
  // Amadeus API (Free tier available)
  AMADEUS: {
    API_KEY: process.env.NEXT_PUBLIC_AMADEUS_API_KEY || 'your_amadeus_api_key',
    API_SECRET: process.env.NEXT_PUBLIC_AMADEUS_API_SECRET || 'your_amadeus_api_secret',
    BASE_URL: 'https://api.amadeus.com/v1',
    ENDPOINTS: {
      FLIGHTS: '/shopping/flight-offers',
      HOTELS: '/shopping/hotel-offers',
      CARS: '/shopping/car-offers'
    }
  },
  
  // Booking.com API (Requires partnership)
  BOOKING: {
    API_KEY: process.env.NEXT_PUBLIC_BOOKING_API_KEY || 'your_booking_api_key',
    BASE_URL: 'https://distribution-xml.booking.com/2.0/json',
    ENDPOINTS: {
      HOTELS: '/hotelAvailability',
      SEARCH: '/hotelSearch'
    }
  },
  
  // Expedia API (Requires partnership)
  EXPEDIA: {
    API_KEY: process.env.NEXT_PUBLIC_EXPEDIA_API_KEY || 'your_expedia_api_key',
    BASE_URL: 'https://api.expedia.com/v1',
    ENDPOINTS: {
      HOTELS: '/hotels/search',
      CARS: '/cars/search',
      ACTIVITIES: '/activities/search'
    }
  },
  
  // GetYourGuide API (Activities/Tours)
  GETYOURGUIDE: {
    API_KEY: process.env.NEXT_PUBLIC_GETYOURGUIDE_API_KEY || 'your_getyourguide_api_key',
    BASE_URL: 'https://api.getyourguide.com/1',
    ENDPOINTS: {
      ACTIVITIES: '/activities'
    }
  },
  
  // Viator API (Activities/Tours)
  VIATOR: {
    API_KEY: process.env.NEXT_PUBLIC_VIATOR_API_KEY || 'your_viator_api_key',
    BASE_URL: 'https://api.viator.com/partner',
    ENDPOINTS: {
      PRODUCTS: '/products/search',
      BOOKING: '/booking'
    }
  }
};

// Helper function to get API headers
export const getApiHeaders = (apiName: keyof typeof API_CONFIG): Record<string, string> => {
  const config = API_CONFIG[apiName];
  
  switch (apiName) {
    case 'AMADEUS':
      return {
        'Authorization': `Bearer ${config.API_KEY}`,
        'Content-Type': 'application/json'
      };
    case 'BOOKING':
      return {
        'X-API-Key': config.API_KEY,
        'Content-Type': 'application/json'
      };
    case 'EXPEDIA':
      return {
        'Authorization': `Bearer ${config.API_KEY}`,
        'Content-Type': 'application/json'
      };
    case 'GETYOURGUIDE':
      return {
        'X-API-Key': config.API_KEY,
        'Content-Type': 'application/json'
      };
    case 'VIATOR':
      return {
        'exp-api-key': config.API_KEY,
        'Content-Type': 'application/json'
      };
    default:
      return {
        'Content-Type': 'application/json'
      };
  }
};

// Rate limiting configuration
export const RATE_LIMITS = {
  AMADEUS: {
    requestsPerSecond: 10,
    requestsPerDay: 2000
  },
  BOOKING: {
    requestsPerSecond: 5,
    requestsPerDay: 1000
  },
  EXPEDIA: {
    requestsPerSecond: 10,
    requestsPerDay: 5000
  }
};
