import math
import requests
from app.config import Config


class GoogleMapsService:
    """Service for interacting with Google Maps API."""
    
    @staticmethod
    def get_api_key():
        """Get the Google Maps API key from configuration."""
        return Config.GOOGLE_MAPS_API_KEY

    @staticmethod
    def get_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return round(km, 2)

    @staticmethod
    def get_distance_matrix(origins, destinations, mode='driving'):
        """
        Get distance matrix using Google Maps Distance Matrix API.
        
        Args:
            origins: Origin address or coordinates
            destinations: Destination address or coordinates
            mode: Travel mode (driving, walking, bicycling, transit)
        
        Returns:
            dict: Distance and duration information
        """
        api_key = GoogleMapsService.get_api_key()
        
        if not api_key:
            # Fallback to Haversine calculation
            if isinstance(origins, str):
                # If origins is an address, return error
                return {'error': 'API key not configured'}
            if isinstance(destinations, str):
                return {'error': 'API key not configured'}
            
            # Calculate using Haversine
            distance = GoogleMapsService.get_distance(
                origins[0], origins[1], destinations[0], destinations[1]
            )
            return {
                'distance': {'text': f'{distance} km', 'value': distance * 1000},
                'duration': {'text': 'Calculated', 'value': distance * 60},  # Rough estimate
                'origin': f"{origins[0]}, {origins[1]}",
                'destination': f"{destinations[0]}, {destinations[1]}"
            }

        base_url = Config.GOOGLE_MAPS_DISTANCE_MATRIX_URL
        
        params = {
            'origins': origins,
            'destinations': destinations,
            'mode': mode,
            'key': api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('status') == 'OK':
                element = data['rows'][0]['elements'][0]
                if element.get('status') == 'OK':
                    return {
                        'distance': element['distance'],
                        'duration': element['duration'],
                        'origin': data.get('origin_addresses', [''])[0],
                        'destination': data.get('destination_addresses', [''])[0]
                    }
                else:
                    return {'error': element.get('status', 'Unknown error')}
            else:
                return {'error': data.get('status', 'API request failed')}
                
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def geocode(address):
        """
        Geocode an address using Google Maps Geocoding API.
        
        Args:
            address: The address to geocode
        
        Returns:
            dict: Geocoded location information
        """
        api_key = GoogleMapsService.get_api_key()
        
        if not api_key:
            return {'error': 'API key not configured'}
        
        base_url = Config.GOOGLE_MAPS_GEOCODING_URL
        
        params = {
            'address': address,
            'key': api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                result = data['results'][0]
                return {
                    'address': result['formatted_address'],
                    'location': result['geometry']['location'],
                    'place_id': result['place_id'],
                    'viewport': result['geometry']['viewport']
                }
            else:
                return {'error': data.get('status', 'Geocoding failed')}
                
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def reverse_geocode(lat, lng):
        """
        Reverse geocode coordinates to an address.
        
        Args:
            lat: Latitude
            lng: Longitude
        
        Returns:
            dict: Reverse geocoded address information
        """
        api_key = GoogleMapsService.get_api_key()
        
        if not api_key:
            return {'error': 'API key not configured'}
        
        base_url = Config.GOOGLE_MAPS_GEOCODING_URL
        
        params = {
            'latlng': f"{lat},{lng}",
            'key': api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                result = data['results'][0]
                return {
                    'address': result['formatted_address'],
                    'place_id': result['place_id'],
                    'location': {'lat': lat, 'lng': lng}
                }
            else:
                return {'error': data.get('status', 'Reverse geocoding failed')}
                
        except Exception as e:
            return {'error': str(e)}
