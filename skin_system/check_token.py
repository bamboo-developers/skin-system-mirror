import json
import os
from fastapi import Request
from fastapi.responses import JSONResponse
from .get_path import get_path
from typing import Literal
from functools import wraps
import asyncio

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
    with open(tokens_path, 'r') as file:
        data = json.load(file)
    return data.get('valid_tokens', {})

def token_required(min_priority, method: Literal["GET", "POST"] = 'GET'):
    def decorator(func):
        @wraps(func)
        async def decorated_function(*args, **kwargs):
            request: Request = kwargs.get('request') or (args[0] if args else None)

            if os.environ.get("TOKEN_SYSTEM") == '0':
                return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

            if method != 'GET':
                form = await request.form()
                token = form.get('token')
            else:
                token = request.query_params.get('token')

            valid_tokens = load_tokens()
            if not token or token not in valid_tokens:
                return JSONResponse({'message': 'Invalid token or token not found', 'code': 401}, status_code=401)

            token_priority = valid_tokens[token].get('priority', 0)
            if token_priority < min_priority:
                return JSONResponse({'message': 'Insufficient token priority', 'code': 403}, status_code=403)

            return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        return decorated_function
    return decorator
