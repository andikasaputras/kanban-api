from flask import Blueprint, jsonify, session, g

from .register_service import create_user
from .login_service import login_user
from app.exceptions.custom_exceptions import \
    UserActionError, InternalServerError
from app.utils.auth_utils import login_required
from app.utils.request_utils import require_json_content


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
@require_json_content
def register():
    if session.get("id"):
        raise UserActionError(
            "You are already logged in. "
            "Please logout to register a new account.")

    response = create_user(g.request_json)

    return jsonify(response), response["status"]


@auth.route("/login", methods=["POST"])
@require_json_content
def login():
    if session.get("id"):
        raise UserActionError(
            "You are already logged in. "
            "Please logout to login to a different account.")

    response = login_user(g.request_json)

    return response, response["status"]


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    try:
        session.clear()
        return jsonify({
            "status": 200,
            "message": "You have been logged out."}), 200
    except Exception as e:
        raise InternalServerError("Error logging out: " + str(e))
