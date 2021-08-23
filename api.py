from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)





api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(debug=True, port=5005)
