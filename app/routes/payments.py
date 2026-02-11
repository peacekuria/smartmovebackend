from flask import Blueprint, request
from app.services.mpesa_service import MpesaService
from app.models.booking import Booking
from app.extensions import db
from app.utils.response import success, error_response as error

# This name must match exactly your app/__init__.py
payment_bp = Blueprint("payments", __name__)


@payment_bp.route("/stk-push", methods=["POST"])
def initiate_payment():
    data = request.get_json()
    phone = data.get("phone")
    amount = data.get("amount")
    booking_id = data.get("booking_id")

    if not all([phone, amount, booking_id]):
        return error("Missing phone, amount, or booking_id", 400)

    booking = Booking.query.get(booking_id)
    if not booking:
        return error("Booking not found", 404)

    # Calling the correct function name from your service
    response = MpesaService.initiate_stk_push(phone, amount, booking_id)

    if response.get("ResponseCode") == "0":
        booking.checkout_request_id = response.get("CheckoutRequestID")
        booking.payment_status = "PENDING"
        db.session.commit()
        return success(data=response, message="STK Push Initiated Successfully")

    return error("STK Push Failed", status_code=400)


@payment_bp.route("/callback", methods=["POST"])
def mpesa_callback():
    """Endpoint where Safaricom sends payment results"""
    data = request.get_json()

    # 0 = Success, anything else = Failure
    result_code = data["Body"]["stkCallback"]["ResultCode"]
    checkout_id = data["Body"]["stkCallback"]["CheckoutRequestID"]

    booking = Booking.query.filter_by(checkout_request_id=checkout_id).first()

    if booking:
        if result_code == 0:
            booking.payment_status = "COMPLETED"
            # Get the Receipt Number from metadata
            items = (
                data["Body"]["stkCallback"].get("CallbackMetadata", {}).get("Item", [])
            )
            for item in items:
                if item["Name"] == "MpesaReceiptNumber":
                    booking.mpesa_receipt_number = item["Value"]
        else:
            booking.payment_status = "FAILED"

        db.session.commit()
    return success(message="Callback processed")
