from fastapi import HTTPException
from starlette import status


class ModelAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_400_BAD_REQUEST, "Model already exists")


class InvalidIdException(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_400_BAD_REQUEST, "Invalid ID")


class ModelDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, "Model not found")


class FileNotFound(HTTPException):
    def __init__(self):
        super().__init__(status.HTTP_404_NOT_FOUND, "File not found")
