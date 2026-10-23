print("Welcome to MAD2 Project")

from flask import Flask, request

app = Flask(__name__)

# implementing jwt auth
from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # better to use environment variable for production
jwt = JWTManager(app)

# Importing and initializing the API from routes.py
from routes import api
api.init_app(app)

# Importing the database models and initializing the database
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return {"message": "Received GET request at /"}
    elif request.method == 'POST':
        return {"message": "Received POST request at /"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_user = User(username='admin', role='admin', email='admin@example.com', password='admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created with username 'admin' and password 'admin123'")
        else:
            print("Admin user already exists with username 'admin' and password 'admin123'")
            
    app.run(debug=True)