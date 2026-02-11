import googlemaps
from flask import current_app


class GoogleMapsService:
    @staticmethod
    def get_road_distance(origin, destination):
        """
        Calculates driving distance and duration.
        'origin' and 'destination' can be addresses or (lat, lng) tuples.
        """
        gmaps = googlemaps.Client(key=current_app.config["GOOGLE_MAPS_API_KEY"])

        try:
            # result is a dictionary containing rows and elements
            matrix = gmaps.distance_matrix(origin, destination, mode="driving")

            if matrix["status"] == "OK":
                element = matrix["rows"][0]["elements"][0]
                if element["status"] == "OK":
                    return {
                        "distance_km": element["distance"]["value"] / 1000,
                        "duration_text": element["duration"]["text"],
                        "status": "success",
                    }
            return {"status": "error", "message": "Could not calculate distance"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
