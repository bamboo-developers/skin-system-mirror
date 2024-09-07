import json
import os
from flask import request
from .get_path import get_path

def load_tokens():
    tokens_path = get_path('tokens.json', '..')

    if not os.path.isfile(tokens_path):
        with open(tokens_path, 'w') as file:
            file.write('''{
  "valid_tokens": {
    "token1": {"priority": 0},
    "token2": {"priority": 1},
    "token3": {"priority": 2}
  }
}
''')
        # raise FileNotFoundError(f"File not found: {tokens_path}")

    with open(tokens_path, 'r') as file:
        data = json.load(file)
    return data.get('valid_tokens', {})

def token_required(min_priority):
    def decorator(func):
        def decorated_function(*args, **kwargs):
            token = request.args.get('token')
            valid_tokens = load_tokens()

            if not token or token not in valid_tokens:
                return {'message': 'Invalid token or token not found'}, 403

            token_priority = valid_tokens[token].get('priority', 0)
            if token_priority < min_priority:
                return {'message': 'Insufficient token priority'}, 403

            return func(*args, **kwargs)
        return decorated_function
    return decorator