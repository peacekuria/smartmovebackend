import requests
import base64
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth


class MpesaService:
    @staticmethod
    def get_token():
        """Fetch OAuth Access Token from Safaricom Sandbox"""
        consumer_key = os.getenv("MPESA_CONSUMER_KEY")
        consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
        api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

        response = requests.get(
            api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret)
        )
        return response.json().get("access_token")

    @staticmethod
    def initiate_stk_push(phone, amount, booking_id):
        """Send the STK Push request to the user's phone"""
        access_token = MpesaService.get_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        shortcode = os.getenv("MPESA_SHORTCODE")
        passkey = os.getenv("MPESA_PASSKEY")

        # Password: Base64(Shortcode + Passkey + Timestamp)
        password_str = f"{shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        headers = {"Authorization": f"Bearer {access_token}"}

        payload = {
            "BusinessShortCode": shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(float(amount)),
            "PhoneNumber": phone,
            "PartyA": phone,
            "PartyB": shortcode,
            # Updated with your active ngrok and '/api' prefix
            "CallBackURL": "https://kaleb-concordant-floyd.ngrok-free.dev/api/payments/callback",
            "AccountReference": f"Booking{booking_id}",
            "TransactionDesc": "Smartmove Payment",
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )
        return response.json()
