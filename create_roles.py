from app import create_app, db
from app.models.user import User, UserRole

app = create_app()
with app.app_context():
    # Create Admin User
    admin_email = "admin@smartmove.com"
    if not User.query.filter_by(email=admin_email).first():
        admin = User(email=admin_email, role=UserRole.ADMIN)
        admin.set_password("password123")
        db.session.add(admin)
        print(f"Created Admin: {admin_email}")
    else:
        print(f"Admin {admin_email} already exists")

    # Create Mover User
    mover_email = "mover@test.com"
    if not User.query.filter_by(email=mover_email).first():
        mover = User(email=mover_email, role=UserRole.MOVER)
        mover.set_password("password123")
        db.session.add(mover)
        print(f"Created Mover: {mover_email}")
    else:
        print(f"Mover {mover_email} already exists")

    db.session.commit()
    print("User creation complete.")
