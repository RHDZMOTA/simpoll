from flask import Blueprint, request, jsonify, make_response

from simpoll.settings import get_logger

logger = get_logger(name=__name__)


# Create blueprint
endpoint_ping = Blueprint(
    "ping",
    __name__,
    url_prefix="/ping"
)

@endpoint_ping.route("/", methods=["GET"])
def ping():
    return make_response(
        jsonify(
            {
                "output": "pong",
            }
        ),
        200
    )
