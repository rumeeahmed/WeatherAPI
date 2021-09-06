from flask_restful import Resource
from flask import jsonify, request
import base64


class Ping(Resource):
    """
    Object that handles the 'ping' endpoint
    """
    def get(self):
        """
        Endpoint to check if the service is working.
        :return: JSON object containing details about the API.
        """
        secret = 'admin:secret'
        auth_header_raw = request.headers.get('Authorization', '')

        if auth_header_raw:
            auth_header = auth_header_raw.strip('Basic ')
            decoded_secret = base64.b64decode(auth_header).decode()

            if decoded_secret == secret:
                ping_dict = {
                    "name": "weatherservice",
                    "status": "ok",
                    "version": "1.0.0"
                }
                return jsonify(ping_dict), 200
            else:
                return {'error': 'Incorrect Password'}, 403

        return {'error': 'No auth credentials in request'}, 401
