from app.models.user import User, UserRole
from app.extensions import db
from flask import current_app
import jwt
import datetime

class AuthService:
    @staticmethod
    def register_user(data):
        email = data.get('email')
        password = data.get('password')
        role_str = data.get('role', 'customer')
        
        # Normalize 'client' to 'customer' for internal consistency
        if role_str == 'client':
            role_str = 'customer'
        
        # Safely convert role string to UserRole enum
        try:
            role = UserRole(role_str)
        except ValueError:
            # Default to CUSTOMER if an invalid role is provided
            role = UserRole.CUSTOMER

        if User.query.filter_by(email=email).first():
            raise Exception("User with this email already exists.")

        new_user = User(
            email=email, 
            role=role,
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user.id,
                'role': user.role.value
            }
            token = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return token, user
        raise Exception("Invalid email or password.")
