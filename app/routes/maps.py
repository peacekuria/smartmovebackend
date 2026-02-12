from flask import Blueprint, request
from app.utils.response import success, error_response
from app.services.google_maps_service import GoogleMapsService
from app.utils.validators import validate_request

maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/distance', methods=['POST'])
def get_distance():
    """
    Get distance between two points using Google Maps API.
    Accepts: origin, destination, and optional mode (driving, walking, bicycling, transit)
    """
    data = request.get_json() if request.is_json else {}
    origin = data.get('origin')
    destination = data.get('destination')
    mode = data.get('mode', 'driving')
    
    if not origin or not destination:
        return error_response('Both origin and destination are required', 400)
    
    try:
        distance_info = GoogleMapsService.get_distance_matrix(origin, destination, mode)
        if 'error' in distance_info:
            return error_response(distance_info['error'], 400)
        return success(distance_info)
    except Exception as e:
        return error_response(str(e), 500)

@maps_bp.route('/geocode', methods=['GET'])
def geocode_address():
    """
    Geocode an address to coordinates using Google Maps API.
    """
    address = request.args.get('address')
    
    if not address:
        return error_response('Address parameter is required', 400)
    
    try:
        result = GoogleMapsService.geocode(address)
        if 'error' in result:
            return error_response(result['error'], 400)
        return success(result)
    except Exception as e:
        return error_response(str(e), 500)

@maps_bp.route('/reverse-geocode', methods=['GET'])
def reverse_geocode_location():
    """
    Reverse geocode coordinates to an address.
    """
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    if not lat or not lng:
        return error_response('Both lat and lng parameters are required', 400)
    
    try:
        lat = float(lat)
        lng = float(lng)
        result = GoogleMapsService.reverse_geocode(lat, lng)
        if 'error' in result:
            return error_response(result['error'], 400)
        return success(result)
    except ValueError:
        return error_response('Invalid coordinates', 400)
    except Exception as e:
        return error_response(str(e), 500)

@maps_bp.route('/config/google-maps-key', methods=['GET'])
def get_google_maps_key():
    """ 
    Returns the Google Maps API key for the frontend.
    """
    from flask import current_app, jsonify
    api_key = current_app.config.get('GOOGLE_MAPS_API_KEY')
    if not api_key:
        return error_response("Google Maps API key not configured", 500)
    return jsonify({"googleMapsApiKey": api_key})
