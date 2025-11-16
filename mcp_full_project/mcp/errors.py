from fastapi import HTTPException

class ApiException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = "internal error"):
        super().__init__(status_code=status_code, detail=detail)
