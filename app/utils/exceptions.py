from http.client import responses
from starlette.responses import JSONResponse


async def my_validation_exception_handler(request, exc):
    return JSONResponse({
        'result': False,
        'error_type': 'validation error',
        'error_message': str(exc)
    }, status_code=422)


async def my_exception_handler(request, exc):
    return JSONResponse({
        'result': False,
        'error_type': responses[exc.status_code],
        'error_message': str(exc.detail)
    }, status_code=exc.status_code)
