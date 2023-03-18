from fastapi import HTTPException, status


class AppError:

    CREDENTIALS_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    NSFW_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="NSFW content was generated, please try again or use another prompt.",
        headers={"WWW-Authenticate": "Bearer"},
    )
