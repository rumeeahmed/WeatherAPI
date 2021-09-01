from flask import Flask
from flask_restful import Api
from routes.forecast import Forecast
from routes.ping import Ping
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)
load_dotenv()

api.add_resource(Ping, '/ping')
api.add_resource(Forecast, '/forecast/<city>')

if __name__ == '__main__':
    app.run(debug=False, port=5005)
