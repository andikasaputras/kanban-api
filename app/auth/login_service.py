import re
import bcrypt

from flask import session

from app.auth.auth_models import User
from app.utils.regexes import RE_EMAIL_VALIDATION
from app.exceptions.custom_exceptions import \
    UserActionError, ValidationError, PasswordMismatchError, NotFoundError


def validate_login(username=None, email=None, password=None):
    # check if user logged in with username
    if username and password:
        # check if username exists
        user = User.get_by_username(username)
        if not user:
            raise NotFoundError(
                "The provided username does not exist. "
                "Please check your spelling or consider registering.")
        # password check
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            raise PasswordMismatchError(
                "The provided password is incorrect. Please try again.")

        return user

    # check if user logged in with email
    elif email and password:
        # email validation
        if not re.search(RE_EMAIL_VALIDATION, email):
            raise ValidationError("The provided email address is not valid. "
                                  "Please enter a valid email address.")
        # check if email exists
        user = User.get_by_email(email)
        if not user:
            raise NotFoundError(
                "The provided email does not exist. "
                "Please check your spelling or consider registering.")
        # password check
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash):
            raise PasswordMismatchError(
                "The provided password is incorrect. Please try again.")

        return user

    # check if username or email is filled out
    else:
        raise UserActionError("Please fill out all required fields.")


def login_user(req_data):
    if not req_data:
        raise UserActionError("No login data received. "
                              "Please provide the required information.")

    if "login_identifier" not in req_data or "password" not in req_data:
        raise UserActionError("Some required fields are missing. "
                              "Please provide all required information.")

    login_identifier = req_data["login_identifier"]
    password = req_data["password"]

    if "@" in login_identifier:
        email = login_identifier
        username = None
    else:
        username = login_identifier
        email = None

    user = validate_login(username, email, password)

    session["id"] = user.id
    session["username"] = user.username
    session["email"] = user.email

    return {
        "status": 200,
        "message": "Login successful.",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }
