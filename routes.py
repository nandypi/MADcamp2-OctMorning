from flask import request
from flask_restful import Api, Resource
from models import db, User, Item
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Api()

class HomeResource(Resource):
    def get(self):
        return {"message": "GET request received at /home"}
    def post(self):
        return {"message": "POST request received at /home"}
    
api.add_resource(HomeResource, '/home')

# auth endpoints

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201

api.add_resource(RegisterResource, '/register')

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return {"message": "Login successful", "access_token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401

api.add_resource(LoginResource, '/login')

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = User.query.get(int(get_jwt_identity()))
        if current_user.role != 'admin':
            return {"message": "Admin privileges required"}, 403
        return fn(*args, **kwargs)
    return wrapper

# user endpoints

class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id=None):
        if item_id is None:
            items = Item.query.all()
            return [item.to_dict() for item in items], 200
        else:
            item = Item.query.get(item_id)
            if item:
                return item.to_dict(), 200
            else:
                return {"message": "Item not found"}, 404

    @admin_required
    def post(self):
        # check if the user is admin
        data = request.get_json()
        # validate data here if needed
        item = Item(**data)
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), 201

    @admin_required
    def put(self, item_id):
        # check if the user is admin
        data = request.get_json()
        item = Item.query.get(item_id)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            db.session.commit()
            return item.to_dict(), 200
        else:
            return {"message": "Item not found"}, 404

    @admin_required
    def delete(self, item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}, 200
        else:
            return {"message": "Item not found"}, 404

api.add_resource(ItemResource, '/items', '/items/<int:item_id>')

