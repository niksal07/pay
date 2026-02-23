from pay_app import app, db
from pay_app.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    admin = User.query.filter_by(username="admin").first()

    if not admin:
        hashed_pw = bcrypt.generate_password_hash("admin123").decode('utf-8')
        
        admin_user = User(
            username="admin",
            email="admin@payapp.com",
            password_hash=hashed_pw,
            role="admin"
        )

        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin already exists!")