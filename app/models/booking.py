# app/models/booking.py
from app.extensions import db
from . import BaseModel
import enum


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_PROGRESS"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Booking(BaseModel):
    __tablename__ = "bookings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    mover_id = db.Column(db.Integer, db.ForeignKey("movers.id"), nullable=True)

    pickup_address = db.Column(db.String, nullable=False)
    dropoff_address = db.Column(db.String, nullable=False)

    booking_time = db.Column(db.DateTime(timezone=True), nullable=False)

    # Changed from db.Enum to db.String for better compatibility
    status = db.Column(db.String(20), default="PENDING", nullable=False)

    distance = db.Column(db.Float, nullable=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    # Payment fields
    mpesa_receipt_number = db.Column(db.String(20), nullable=True)
    payment_status = db.Column(db.String(20), default="PENDING", nullable=False)
    checkout_request_id = db.Column(db.String(50), nullable=True)

    user = db.relationship("User", backref="bookings")
    mover = db.relationship("Mover", backref="bookings")
