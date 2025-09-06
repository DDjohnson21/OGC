# Travel API Integration Guide

This document explains how to integrate real travel APIs into the OGC application for live flight, hotel, car rental, and activity recommendations.

## 🚀 Quick Start

The application currently uses mock data for demonstration purposes. To enable real API integrations:

1. **Get API Keys** from the providers below
2. **Set Environment Variables** in your `.env.local` file
3. **Uncomment API calls** in the code
4. **Deploy** with your API keys

## 🔑 Required API Keys

### 1. Amadeus API (Flights & Hotels)
- **Free Tier**: 2,000 requests/month
- **Sign up**: [Amadeus for Developers](https://developers.amadeus.com/)
- **Setup**:
  ```bash
  NEXT_PUBLIC_AMADEUS_API_KEY=your_api_key
  NEXT_PUBLIC_AMADEUS_API_SECRET=your_api_secret
  ```

### 2. Booking.com API (Hotels)
- **Requires**: Partnership agreement
- **Sign up**: [Booking.com Partner Hub](https://partner.booking.com/)
- **Setup**:
  ```bash
  NEXT_PUBLIC_BOOKING_API_KEY=your_api_key
  ```

### 3. Expedia API (Hotels, Cars, Activities)
- **Requires**: Partnership agreement
- **Sign up**: [Expedia Partner Central](https://partner.expedia.com/)
- **Setup**:
  ```bash
  NEXT_PUBLIC_EXPEDIA_API_KEY=your_api_key
  ```

### 4. GetYourGuide API (Activities)
- **Free Tier**: 1,000 requests/month
- **Sign up**: [GetYourGuide API](https://api.getyourguide.com/)
- **Setup**:
  ```bash
  NEXT_PUBLIC_GETYOURGUIDE_API_KEY=your_api_key
  ```

### 5. Viator API (Activities)
- **Free Tier**: 500 requests/month
- **Sign up**: [Viator API](https://developer.viator.com/)
- **Setup**:
  ```bash
  NEXT_PUBLIC_VIATOR_API_KEY=your_api_key
  ```

## 🔧 Configuration

### Environment Variables
Create a `.env.local` file in your project root:

```bash
# Amadeus API
NEXT_PUBLIC_AMADEUS_API_KEY=your_amadeus_api_key
NEXT_PUBLIC_AMADEUS_API_SECRET=your_amadeus_api_secret

# Booking.com API
NEXT_PUBLIC_BOOKING_API_KEY=your_booking_api_key

# Expedia API
NEXT_PUBLIC_EXPEDIA_API_KEY=your_expedia_api_key

# GetYourGuide API
NEXT_PUBLIC_GETYOURGUIDE_API_KEY=your_getyourguide_api_key

# Viator API
NEXT_PUBLIC_VIATOR_API_KEY=your_viator_api_key
```

### Enable Real API Calls

In `src/lib/api/travelApi.ts`, uncomment the real API calls:

```typescript
// Change this:
return this.generateMockFlights(origin, destination, departureDate, returnDate, passengers);

// To this:
return await this.searchFlightsAmadeus(origin, destination, departureDate, returnDate, passengers);
```

## 📊 API Features

### Flights (Amadeus)
- ✅ Real-time flight search
- ✅ Price comparison
- ✅ Multiple airlines
- ✅ Stop information
- ✅ Aircraft details
- ✅ Class options

### Hotels (Amadeus/Booking.com)
- ✅ Hotel search by location
- ✅ Price comparison
- ✅ Star ratings
- ✅ Amenities
- ✅ Availability
- ✅ Photos

### Car Rentals (Expedia)
- ✅ Car search by location
- ✅ Vehicle details
- ✅ Price comparison
- ✅ Pickup/dropoff locations
- ✅ Features and amenities

### Activities (GetYourGuide/Viator)
- ✅ Activity search
- ✅ Price comparison
- ✅ Reviews and ratings
- ✅ Duration and availability
- ✅ Meeting points
- ✅ Cancellation policies

## 🛠️ Implementation Details

### Rate Limiting
Each API has rate limits. The application includes rate limiting configuration:

```typescript
export const RATE_LIMITS = {
  AMADEUS: {
    requestsPerSecond: 10,
    requestsPerDay: 2000
  },
  // ... other APIs
};
```

### Error Handling
The application gracefully falls back to mock data if API calls fail:

```typescript
try {
  return await this.searchFlightsAmadeus(...);
} catch (error) {
  console.error('API Error:', error);
  return this.generateMockFlights(...); // Fallback
}
```

### Data Transformation
API responses are transformed to a consistent format:

```typescript
// Amadeus response → Our format
{
  id: `flight-${index + 1}`,
  airline: firstSegment.carrierCode,
  price: parseFloat(offer.price.total),
  // ... other fields
}
```

## 🚀 Deployment

### Vercel
1. Add environment variables in Vercel dashboard
2. Deploy your application
3. APIs will work in production

### Other Platforms
1. Set environment variables in your hosting platform
2. Ensure API keys are properly configured
3. Test API calls in production

## 🔒 Security

### API Key Protection
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly
- Monitor API usage

### Rate Limiting
- Implement client-side rate limiting
- Use caching to reduce API calls
- Monitor API usage and costs

## 📈 Monitoring

### API Usage
- Monitor request counts
- Track error rates
- Set up alerts for rate limits
- Log API responses for debugging

### Performance
- Cache frequently requested data
- Implement loading states
- Handle network errors gracefully
- Optimize API calls

## 🧪 Testing

### Mock Data
The application includes comprehensive mock data for testing:
- 5 flight options per search
- 6 hotel options per search
- 4 car rental options per search
- 6 activity options per search

### API Testing
Test real API integrations:
1. Set up API keys
2. Enable real API calls
3. Test with different search parameters
4. Verify data transformation
5. Check error handling

## 📚 Additional Resources

- [Amadeus API Documentation](https://developers.amadeus.com/)
- [Booking.com API Documentation](https://developers.booking.com/)
- [Expedia API Documentation](https://developer.expedia.com/)
- [GetYourGuide API Documentation](https://api.getyourguide.com/)
- [Viator API Documentation](https://developer.viator.com/)

## 🤝 Support

For API integration support:
1. Check API documentation
2. Review error logs
3. Test with mock data first
4. Contact API providers for issues
5. Check rate limits and quotas

---

**Note**: This application is designed for demonstration purposes. For production use, ensure proper API key management, error handling, and compliance with API terms of service.
