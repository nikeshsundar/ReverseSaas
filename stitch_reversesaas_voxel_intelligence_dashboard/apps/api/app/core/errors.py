from fastapi import HTTPException


def not_found(entity: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"{entity} not found")


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail=message)


def too_many_requests(message: str) -> HTTPException:
    return HTTPException(status_code=429, detail=message)
