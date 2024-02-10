import re
import bcrypt

from app.auth.auth_models import User
from app.exceptions.custom_exceptions import \
    ValidationError, UserActionError, AlreadyExistsError
from app.utils.regexes import \
    RE_USERNAME_VALIDATION, RE_EMAIL_VALIDATION, RE_PASSWORD_VALIDATION


def validate_registration(username, email, password, confirm_password):
    # check if all fields are filled out
    if not username or not email or not password or not confirm_password:
        raise UserActionError(
            "Please fill out all required fields.")
    # username validation
    if len(username) < 3:
        raise ValidationError(
            "The username must be at least 3 characters long.")
    if not re.search(RE_USERNAME_VALIDATION, username):
        raise ValidationError(
            "The username can only include letters, "
            "numbers, underscores, and periods.")
    # check if username exists
    user = User.get_by_username(username)
    if user:
        raise AlreadyExistsError(
            "The provided username is already in use. "
            "Please try a different one.")

    # email validation
    if not re.search(RE_EMAIL_VALIDATION, email):
        raise ValidationError(
            "The provided email address is not valid. "
            "Please enter a valid email address.")
    # check if email exists
    user = User.get_by_email(email)
    if user:
        raise AlreadyExistsError(
            "The provided email is already in use. If you forgot "
            "your password, please use the password reset function.")

    # password validation
    if password != confirm_password:
        raise ValidationError(
            "The provided passwords do not match. "
            "Please ensure both passwords are identical.")
    if len(password) < 8:
        raise ValidationError(
            "The password must be at least 8 characters long.")
    if not re.search(RE_PASSWORD_VALIDATION, password):
        raise ValidationError(
            "The password must contain at least one uppercase letter, "
            "one lowercase letter, and one number.")


def create_user(req_data):
    if not req_data:
        raise UserActionError(
            "No registration data received. "
            "Please provide the required information.")

    if ("username" not in req_data
            or "email" not in req_data
            or "password" not in req_data
            or "confirm_password" not in req_data):
        raise UserActionError(
            "Some required fields are missing. "
            "Please provide all required information.")

    username = req_data["username"]
    email = req_data["email"]
    password = req_data["password"]
    confirm_password = req_data["confirm_password"]

    validate_registration(username, email, password, confirm_password)

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt())

    User.create(username, email, password_hash)

    return {
        "status": 201,
        "message": "You have been registered. Please log in."
    }
