from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

app = Flask(__name__)


@app.route('/ping')
def ping():
    """
    Endpoint to check if the service is working.
    :return: JSON object containing details about the API.
    """
    ping_dict = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    return jsonify(ping=ping_dict)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
