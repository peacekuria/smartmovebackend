from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email="alvin@example.com").first()
    if user:
        user.set_password("password123")
        db.session.commit()
        print(f"Password reset for {user.email}")
    else:
        print("User not found")
