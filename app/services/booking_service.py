from datetime import datetime
import os
import requests
from app.models.booking import Booking
from app.extensions import db

class BookingService:
    @staticmethod
    def create_booking(current_user, data):
        pickup = data.get('pickup_address')
        dropoff = data.get('dropoff_address')
        raw_date = data.get('booking_time')

        try:
            booking_time = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            try:
                # Try common ISO formats if the simple one fails
                booking_time = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
            except:
                raise Exception(
                    f"Invalid date format: {raw_date}. Expected YYYY-MM-DD HH:MM:SS"
                )

        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        google_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={pickup}&destinations={dropoff}&key={api_key}"
        response = requests.get(google_url).json()

        if response.get("status") == "OK":
            element = response["rows"][0]["elements"][0]
            if element.get("status") == "ZERO_RESULTS":
                raise Exception(
                    "Could not find a driving route between these locations."
                )

            distance_km = element["distance"]["value"] / 1000
            price_per_km = 150
            total_price = distance_km * price_per_km

            new_booking = Booking(
                user_id=current_user.id,
                pickup_address=pickup,
                dropoff_address=dropoff,
                booking_time=booking_time,
                distance=distance_km,
                total_price=total_price,
                status="pending",
            )

            db.session.add(new_booking)
            db.session.commit()
            return new_booking
        else:
            raise Exception(
                f"Google API Error: {response.get('error_message', 'Unknown error')}"
            )

    @staticmethod
    def get_booking_by_id(booking_id, current_user):
        booking = Booking.query.get(booking_id)
        if not booking:
            raise Exception("Booking not found")
        # Optional: check if current_user has access
        return booking

    @staticmethod
    def get_mover_location(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            raise Exception("Booking not found")
        
        if not booking.mover:
            return {"status": "unassigned"}
        
        mover = booking.mover
        return {
            "status": "assigned",
            "lat": mover.last_lat,
            "lng": mover.last_lng,
            "last_update": mover.last_location_update.isoformat() if mover.last_location_update else None,
            "mover_name": mover.company_name or mover.user.email
        }
