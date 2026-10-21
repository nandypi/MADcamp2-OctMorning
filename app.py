print("Welcome to MAD2 Project")

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return {"message": "Received GET request at /"}
    elif request.method == 'POST':
        return {"message": "Received POST request at /"}

class HomeResource(Resource):
    def get(self):
        return {"message": "GET request received at /home"}
    def post(self):
        return {"message": "POST request received at /home"}

api.add_resource(HomeResource, '/home')

if __name__ == '__main__':
    app.run(debug=True)