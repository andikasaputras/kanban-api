import bcrypt

from app.auth.auth_models import User


# Test case 1: Valid user registration
def test_valid_create_user(test_client):
    with test_client as c:
        new_user = {
            "username": "test_user1",
            "email": "test1@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 201,
            "message": "You have been registered. Please log in."
        }
        assert response.status_code == 201

        # Verify that the user is created in the database
        user = User.get_by_username("test_user1")
        assert user.username == "test_user1"
        assert user.email == "test1@example.com"
        assert bcrypt.checkpw(
            "Password123".encode("utf-8"),
            user.password_hash)


# Test case 2: Invalid user registration when already logged in
def test_invalid_create_user_when_already_logged_in(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user",
            "password": "Password123",
        }
        c.post("/auth/login", json=new_user)

        new_user = {
            "username": "test_user2",
            "email": "test2@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }

        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("You are already logged in. "
                        "Please logout to register a new account.")
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" in sess
            sess.clear()


# Test case 3: Invalid user registration (content type)
def test_invalid_create_user_invalid_content_type(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user3",
            "email": "test3@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register",
                          json=new_user,
                          content_type="text/html")
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "Invalid content type. Please send JSON."
        }
        assert response.status_code == 400


# Test case 4: Invalid user registration (no data received)
def test_invalid_create_user_no_data_received(user_created):
    with user_created as c:
        new_user = {}
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("No registration data received. "
                        "Please provide the required information.")
        }
        assert response.status_code == 400


# Test case 5: Invalid user registration (missing fields)
def test_invalid_create_user_missing_fields(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user5",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("Some required fields are missing. "
                        "Please provide all required information.")
        }
        assert response.status_code == 400


# Test case 6: Invalid user registration (empty fields)
def test_invalid_create_user_empty_fields(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user6",
            "email": "",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "Please fill out all required fields."
        }
        assert response.status_code == 400


# Test case 7: Invalid user registration (username validation)
def test_invalid_create_user_invalid_username(user_created):
    with user_created as c:
        new_user = {
            "username": "te",
            "email": "test7@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "The username must be at least 3 characters long."
        }
        assert response.status_code == 400


# Test case 8: Invalid user registration (username must only contain
# letters, numbers, underscores, and periods)
def test_invalid_create_user_invalid_username_characters(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user@",
            "email": "test8@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("The username can only include letters, "
                        "numbers, underscores, and periods.")
        }
        assert response.status_code == 400


# Test case 9: Invalid user registration (taken username)
def test_invalid_create_user_taken_username(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user",
            "email": "test9@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 409,
            "error": "Conflict",
            "message": ("The provided username is already in use. "
                        "Please try a different one.")
        }
        assert response.status_code == 409


# Test case 10: Invalid user registration (email validation)
def test_invalid_create_user_invalid_email(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user10",
            "email": "xxxx@xxxxxxx",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("The provided email address is not valid. "
                        "Please enter a valid email address.")
        }
        assert response.status_code == 400


# Test case 11: Invalid user registration (taken email)
def test_invalid_create_user_taken_email(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user11",
            "email": "test@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 409,
            "error": "Conflict",
            "message": (
                "The provided email is already in use. If you forgot "
                "your password, please use the password reset function.")
        }
        assert response.status_code == 409


# Test case 12: Invalid user registration (passwords do not match)
def test_invalid_create_user_passwords_do_not_match(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user12",
            "email": "test12@example.com",
            "password": "Password123",
            "confirm_password": "Password12"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("The provided passwords do not match. "
                        "Please ensure both passwords are identical.")
        }
        assert response.status_code == 400


# Test case 13: Invalid user registration (password at least 8 characters)
def test_invalid_create_user_password_too_short(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user13",
            "email": "test13@example.com",
            "password": "Pass1",
            "confirm_password": "Pass1"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "The password must be at least 8 characters long."
        }
        assert response.status_code == 400


# Test case 14: Invalid user registration (password must contain
# at least 1 uppercase letter, 1 lowercase letter, and 1 number)
def test_invalid_create_user_invalid_password(user_created):
    with user_created as c:
        new_user = {
            "username": "test_user14",
            "email": "test14@example.com",
            "password": "password",
            "confirm_password": "password"
        }
        response = c.post("/auth/register", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": (
                "The password must contain at least one uppercase letter, "
                "one lowercase letter, and one number.")
        }
        assert response.status_code == 400
