# Test case 1: Invalid route
def test_invalid_route(test_client):
    with test_client as c:
        response = c.get("/Not-Found-Route")
        assert response.json == {
            "status": 404,
            "error": "Not Found",
            "message": "The requested resource was not found."
        }
        assert response.status_code == 404


# Test case 2: Invalid method
def test_invalid_method(test_client):
    with test_client as c:
        response = c.get("/auth/login")
        assert response.json == {
            "status": 405,
            "error": "Method Not Allowed",
            "message": "The method is not allowed for the requested URL."
        }
        assert response.status_code == 405
