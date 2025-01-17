from app import create_app
from app.extensions import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        from app.models import User, Role

        if not User.query.filter_by(role=Role.ADMIN).first():
            admin_user = User(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                role=Role.ADMIN,
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)
