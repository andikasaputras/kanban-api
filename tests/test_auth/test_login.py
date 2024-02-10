# Test case 1: Valid user login with email
def test_valid_user_login_with_email(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test@example.com",
            "password": "Password123"
        }

        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 200,
            "message": "Login successful.",
            "user": {
                "username": "test_user",
                "email": "test@example.com"
            }
        }
        assert response.status_code == 200
        with c.session_transaction() as sess:
            assert "id" in sess
            sess.clear()


# Test case 2: Valid user login with username
def test_valid_user_login_with_username(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user",
            "password": "Password123"
        }

        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 200,
            "message": "Login successful.",
            "user": {
                "username": "test_user",
                "email": "test@example.com"
            }
        }
        assert response.status_code == 200
        with c.session_transaction() as sess:
            assert "id" in sess
            sess.clear()


# Test case 3: Invalid user login when already logged in
def test_invalid_user_login_when_already_logged_in(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user",
            "password": "Password123"
        }
        c.post("/auth/login", json=new_user)

        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("You are already logged in. "
                        "Please logout to login to a different account.")
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" in sess
            sess.clear()


# Test case 4: Invalid user login (content-type)
def test_invalid_user_login_invalid_content_type(user_created):
    with user_created as c:
        new_user = None
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "Invalid content type. Please send JSON."
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 5: Invalid user login (no data received)
def test_invalid_user_login_no_data_received(user_created):
    with user_created as c:
        new_user = {}
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("No login data received. "
                        "Please provide the required information.")
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 6: Invalid user login (eissing fields)
def test_invalid_user_login_missing_fields(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user"
        }
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("Some required fields are missing. "
                        "Please provide all required information.")
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 7: Invalid user login (empty fields)
def test_invalid_user_login_empty_fields(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "",
            "password": ""
        }

        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "Please fill out all required fields."
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 8: Invalid user login (email validation)
def test_invalid_user_login_invalid_email(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test@examplecom",
            "password": "Password123"
        }
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": ("The provided email address is not valid. "
                        "Please enter a valid email address.")
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 9: Invalid user login (incorrect password with username)
def test_invalid_user_login_incorrect_password_with_username(
        user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user",
            "password": "Password1234"
        }

        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "The provided password is incorrect. Please try again."
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 10: Invalid user login (incorrect password with email)
def test_invalid_user_login_incorrect_password_with_email(
        user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test@example.com",
            "password": "Password1234"
        }
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 400,
            "error": "Bad Request",
            "message": "The provided password is incorrect. Please try again."
        }
        assert response.status_code == 400
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 11: Invalid user login (username does not exist)
def test_invalid_user_login_username_does_not_exist(
        user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user2",
            "password": "Password123"
        }
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 404,
            "error": "Not Found",
            "message": ("The provided username does not exist. "
                        "Please check your spelling or consider registering.")
        }
        assert response.status_code == 404
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 12: Invalid user login (email does not exist)
def test_invalid_user_login_email_does_not_exist(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test2@example.com",
            "password": "Password123"
        }
        response = c.post("/auth/login", json=new_user)
        assert response.json == {
            "status": 404,
            "error": "Not Found",
            "message": ("The provided email does not exist. "
                        "Please check your spelling or consider registering.")
        }
        assert response.status_code == 404
        with c.session_transaction() as sess:
            assert "id" not in sess


# Test case 13: Invalid user access when not logged in
def test_invalid_user_access_when_not_user_created(user_created):
    with user_created as c:
        response = c.get("/auth/logout")
        assert response.json == {
            "status": 401,
            "error": "Unauthorized",
            "message": "Please log in to access this resource."
        }
        assert response.status_code == 401
        with c.session_transaction() as sess:
            assert "id" not in sess
            assert "username" not in sess
            assert "email" not in sess


# Test case 14: Valid user logout
def test_valid_user_logout(user_created):
    with user_created as c:
        new_user = {
            "login_identifier": "test_user",
            "password": "Password123"
        }
        c.post("/auth/login", json=new_user)

        response = c.get("/auth/logout")
        assert response.json == {
            "status": 200,
            "message": "You have been logged out."
        }
        assert response.status_code == 200
        with c.session_transaction() as sess:
            assert "id" not in sess
            assert "username" not in sess
            assert "email" not in sess
            sess.clear()
