from flask import Blueprint, request
from app.services.booking_service import BookingService
from app.services.google_maps_service import GoogleMapsService  # Added this
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required
from app.utils.validators import validate_request

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")

# app/routes/bookings.py


@booking_bp.route("", methods=["POST"])
@jwt_required
@validate_request("pickup_address", "dropoff_address", "booking_time")
def create_booking(current_user):
    data = request.get_json()

    try:
        # 1. Get road distance and duration from Google
        route_info = GoogleMapsService.get_road_distance(
            data["pickup_address"], data["dropoff_address"]
        )

        if route_info["status"] != "success":
            return error_response("Could not calculate distance between addresses", 400)

        # 2. Calculate dynamic price (Example: 2000 base + 50 per km)
        distance_km = route_info["distance_km"]
        estimated_price = 2000 + (distance_km * 50)

        # 3. Add these calculated values to the data dictionary
        data["distance"] = distance_km
        data["duration"] = route_info["duration_text"]
        data["price"] = estimated_price

        # 4. FIX: Swap the arguments to match the Service definition
        # WAS: booking = BookingService.create_booking(current_user, data)
        booking = BookingService.create_booking(data, current_user)

        return success(booking.to_dict(), 201)

    except Exception as e:
        return error_response(str(e))
