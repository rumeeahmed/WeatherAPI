from resources.forecast import Forecast
from resources.ping import Ping
from dotenv import load_dotenv
from flask_restful import Api
from flask import Flask

app = Flask(__name__)
api = Api(app)
load_dotenv()

api.add_resource(Ping, '/ping')
api.add_resource(Forecast, '/forecast/<string:city>')

if __name__ == '__main__':
    app.run(debug=False, port=5005)
