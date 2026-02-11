import requests
import os
from datetime import datetime
from app.models.booking import Booking
from app.extensions import db


class BookingService:
    @staticmethod
    def create_booking(data, current_user):
        pickup = data.get("pickup_address")
        dropoff = data.get("dropoff_address")
        raw_date = data.get("booking_time")

        try:
            booking_time = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
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
                status="pending",  # Simple string matches the new model
            )

            db.session.add(new_booking)
            db.session.commit()
            return new_booking
        else:
            raise Exception(
                f"Google API Error: {response.get('error_message', 'Unknown error')}"
            )
