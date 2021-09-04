from flask_restful import Resource
from flask import jsonify


class Ping(Resource):
    """
    Object that handles the 'ping' endpoint
    """
    def get(self):
        """
        Endpoint to check if the service is working.
        :return: JSON object containing details about the API.
        """
        ping_dict = {
            "name": "weatherservice",
            "status": "ok",
            "version": "1.0.0"
        }
        return jsonify(ping_dict)
