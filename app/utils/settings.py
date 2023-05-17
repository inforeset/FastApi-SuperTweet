import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field

MEDIA_ROOT = './media'
BASE_DIR = Path(__file__).resolve().parent.parent.parent

RESPONSE_401 = {
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "example": {'result': False,
                            'error_type': 'Unauthorized',
                            'error_message': 'Not authenticated'}
            }
        },
    }
}

RESPONSE_401_422 = {
    **RESPONSE_401,
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {'result': False,
                            'error_type': 'validation error',
                            'error_message': 'validation error message'}
            }
        },
    },
}

RESPONSE_401_422_404 = {
    **RESPONSE_401_422,
    404: {
        "description": "Not found",
        "content": {
            "application/json": {
                "example": {'result': False,
                            'error_type': 'not found',
                            'error_message': 'not found element'}
            }
        },
    },
}

RESPONSE_401_422_404_403 = {
    **RESPONSE_401_422_404,
    403: {
        "description": "Access forbidden",
        "content": {
            "application/json": {
                "example": {'result': False,
                            'error_type': 'Access error',
                            'error_message': 'Access forbidden'}
            }
        },
    },
}

RESPONSE_401_422_404_400 = {
    **RESPONSE_401_422_404,
    400: {
        "description": "Bad request",
        "content": {
            "application/json": {
                "example": {'result': False,
                            'error_type': 'Bad request',
                            'error_message': "Can't follow yourself"}
            }
        },
    },
}


class Settings(BaseSettings):
    db_host: str = Field(..., env="POSTGRES_HOST")
    db_user: str = Field(..., env="POSTGRES_USER")
    db_name: str = Field(..., env="POSTGRES_DB")
    db_port: str = Field(..., env="POSTGRES_PORT")
    db_password: str = Field(..., env="POSTGRES_PASSWORD")
    db_test_name: str = Field(..., env="POSTGRES_DB_FOR_TESTS")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = os.path.join(BASE_DIR, '.env')
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()

