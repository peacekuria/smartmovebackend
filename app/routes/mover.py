from flask import Blueprint, request
from app.services.mover_service import MoverService
from app.utils.response import success, error_response
from app.utils.decorators import jwt_required, roles_required

mover_bp = Blueprint('mover', __name__, url_prefix='/movers')

@mover_bp.route('/profile', methods=['PUT'])
@jwt_required
@roles_required('mover')
def update_mover_profile(current_user):
    data = request.get_json()
    try:
        mover = MoverService.update_mover_profile(current_user.mover.id, data)
        return success(mover.to_dict())
    except Exception as e:
        return error_response(str(e))

@mover_bp.route('/availability', methods=['GET'])
@jwt_required
@roles_required('mover')
def get_availability(current_user):
    try:
        availability = MoverService.get_availability(current_user.mover.id)
        return success(availability)
    except Exception as e:
        return error_response(str(e))

@mover_bp.route('/location', methods=['POST'])
@jwt_required
@roles_required('mover')
def update_location(current_user):
    data = request.get_json()
    lat = data.get('lat')
    lng = data.get('lng')
    
    if lat is None or lng is None:
        return error_response("Latitude and Longitude are required", 400)
    
    try:
        MoverService.update_mover_location(current_user.mover.id, lat, lng)
        return success(message="Location updated")
    except Exception as e:
        return error_response(str(e))
