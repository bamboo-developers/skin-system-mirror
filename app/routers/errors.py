from fastapi import Request
from fastapi.responses import JSONResponse

async def handle_error(request: Request, e: Exception):
    status_code = 500
    if hasattr(e, 'status_code'):
        status_code = e.status_code
    return JSONResponse({'message': str(e), 'code': status_code}, status_code=status_code)
