from app.extensions import db
from app.models.mover import Mover
import datetime

class MoverService:
    @staticmethod
    def update_mover_profile(mover_id, data):
        mover = Mover.query.get(mover_id)
        if not mover:
            raise Exception("Mover not found")
        
        for key, value in data.items():
            if hasattr(mover, key):
                setattr(mover, key, value)
        
        db.session.commit()
        return mover

    @staticmethod
    def get_availability(mover_id):
        mover = Mover.query.get(mover_id)
        if not mover:
            raise Exception("Mover not found")
        return {"approved": mover.approved}

    @staticmethod
    def update_mover_location(mover_id, lat, lng):
        mover = Mover.query.get(mover_id)
        if not mover:
            raise Exception("Mover not found")
        
        mover.last_lat = lat
        mover.last_lng = lng
        mover.last_location_update = datetime.datetime.utcnow()
        
        db.session.commit()
        return mover
