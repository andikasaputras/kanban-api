from http.client import responses

from flask import jsonify
from app.exceptions.custom_exceptions import \
    ClientError, InternalServerError


def init_errorhandlers(app):
    @app.errorhandler(ClientError)
    def handle_client_error(error):
        response = jsonify({
          "status": int(error.status_code),
          "error": str(responses[error.status_code]),
          "message": str(error.message)})
        response.status_code = error.status_code
        return response

    @app.errorhandler(400)
    def handle_bad_request(e):
        response = jsonify({
            "status": 400,
            "error": "Bad Request",
            "message": ("The browser (or proxy) sent a request "
                        "that this server could not understand.")})
        response.status_code = 400
        return response

    @app.errorhandler(404)
    def handle_not_found(e):
        response = jsonify({
            "status": 404,
            "error": "Not Found",
            "message": "The requested resource was not found."})
        response.status_code = 404
        return response

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        response = jsonify({
            "status": 405,
            "error": "Method Not Allowed",
            "message": "The method is not allowed for the requested URL."})
        response.status_code = 405
        return response

    @app.errorhandler(501)
    def handle_not_implemented(e):
        response = jsonify({
            "status": 501,
            "error": "Not Implemented",
            "message": ("The server does not support "
                        "the action requested by the browser.")})
        response.status_code = 501
        return response

    @app.errorhandler(503)
    def handle_service_unavailable(e):
        response = jsonify({
            "status": 503,
            "error": "Service Unavailable",
            "message": (
                "The server is currently unable to handle the request due to"
                "a temporary overloading or maintenance of the server.")})
        response.status_code = 503
        return response

    @app.errorhandler(InternalServerError)
    def handle_internal_server_error(error):
        responses = jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again."})
        responses.status_code = 500
        app.logger.error(f"{type(error).__name__}: {str(error)}")
        return responses

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        response = jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again."})
        response.status_code = 500
        app.logger.error(f"{type(error).__name__}: {str(error)}")
        return response
