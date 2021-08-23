from flask import Flask
from flask_restful import Api
from routes.ping import Ping
from routes.forecast import Forecast

app = Flask(__name__)
api = Api(app)

api.add_resource(Ping, '/ping')
api.add_resource(Forecast, '/forecast/<city>')

if __name__ == '__main__':
    app.run(debug=True, port=5005)
