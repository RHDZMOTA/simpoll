from flask import Blueprint, request, jsonify, make_response

from simpoll.models import Question, Option
from simpoll.settings import get_logger

logger = get_logger(name=__name__)


# Create blueprint
endpoint_question = Blueprint(
    "question",
    __name__,
    url_prefix="/question"
)

@endpoint_question.route("/create", methods=["GET"])
def question_create():
    question = Question(
        question=request.args.get("question"),
        description=request.args.get("description"),
        correct_choices=int(request.args.get("correct_choices", "0")),
        metadata={
            "remote_addr": request.remote_addr
        },
    )
    logger.warning("Question created")
    return make_response(
        jsonify(
            {
                "short_id": question.short_id,
                "created_at": question.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        ),
        200
    )

@endpoint_question.route("/add_option", methods=["GET"])
def option_add():
    pass