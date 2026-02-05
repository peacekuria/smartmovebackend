from app.models.booking import Booking
from app.extensions import db


def test_booking_creation(app):
    booking = Booking(user_id=1, mover_id=2, total_price=15000.0, status="pending")
    db.session.add(booking)
    db.session.commit()
    assert booking.id is not None
    assert booking.total_price == 15000.0
