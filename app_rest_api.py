
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from functools import wraps
import jwt_validator
from custom_auth_handler import AuthHandler
import open_ai_chat_completion

# MSAL Configuration Expires 30/04/2024
app = Flask(__name__)
CORS(app)

decoded_token  = None

# Error handler


@app.errorhandler(AuthHandler)
def handle_auth_error(e):
    """
    Error handler for AuthError exceptions.
    """
    response = jsonify(e.to_dict())
    response.status_code = e.status_code
    return response



def get_auth_token_header() -> str:
        token = request.headers.get('Authorization')  # Get the token from the header
        if not token:
            return jsonify({"error": "No token provided"}), 401

        parts = token.split()
        if parts[0].lower() != "bearer":
            raise AuthHandler({"code": "invalid_header",
                            "description":
                                "Authorization header must start with"
                                " Bearer"}, 401)
        elif len(parts) == 1:
            raise AuthHandler({"code": "invalid_header",
                            "description": "Token not found"}, 401)
        elif len(parts) > 2:
            raise AuthHandler({"code": "invalid_header",
                            "description":
                                "Authorization header must be"
                                " Bearer token"}, 401)
        
        token = parts[1]  # Remove 'Bearer ' from token
        return token



def validate_jwt_request_(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = get_auth_token_header()
        decoded_token = jwt_validator.validate_jwt(token)
        print(decoded_token)
    
    return decorator




@app.route('/send', methods=['get'])
@validate_jwt_request_
def send_message():
    """ Endpoint to receive user messages and start streaming responses. """
    user_message = request.args.get("message")
    print(user_message + "\n")

    # Ensure message is not empty
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = open_ai_chat_completion.generate_response(user_message)
    return jsonify({"response": response})



if __name__ == '__main__':
    app.register_error_handler(AuthHandler, handle_auth_error)
    app.run(debug=True)
