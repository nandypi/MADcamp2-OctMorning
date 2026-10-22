from flask import request
from flask_restful import Api, Resource
from models import db, User, Item

api = Api()

class HomeResource(Resource):
    def get(self):
        return {"message": "GET request received at /home"}
    def post(self):
        return {"message": "POST request received at /home"}
    
api.add_resource(HomeResource, '/home')

class ItemResource(Resource):
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

    def post(self):
        data = request.get_json()
        # validate data here if needed
        item = Item(**data)
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), 201

    def put(self, item_id):
        data = request.get_json()
        item = Item.query.get(item_id)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            db.session.commit()
            return item.to_dict(), 200
        else:
            return {"message": "Item not found"}, 404

    def delete(self, item_id):
        item = Item.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted"}, 200
        else:
            return {"message": "Item not found"}, 404

api.add_resource(ItemResource, '/items', '/items/<int:item_id>')

