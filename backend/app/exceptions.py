from fastapi import HTTPException, status


class AppError:

    CREDENTIALS_ERROR = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    INVALID_TIME_ARGS = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Date format is YYYY-MM-DD.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    USERNAME_EXISTS_ERROR = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Credentials already exists.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    WRONG_PASSWORD_ERROR = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    POST_NOT_FOUND = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post with given post_id does not exist.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    MISSING_POST_ID = HTTPException(
        status_code=404,
        detail="There are no processed post with such post ID.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    INVALID_ID = HTTPException(
        status_code=400,
        detail="The ID you've provided is invalid.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    SENTIMENT_CHANGELOG_ALREADY_EXISTS = HTTPException(
        status_code=409,
        detail="This sentiment changelog already exists in the database.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    NO_POST_DATA_FOUND = HTTPException(
        status_code=404,
        detail="There are no post data available.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    TAG_ALREADY_EXISTS = HTTPException(
        status_code=409,
        detail="This tag already exists in the database.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    DATA_ALREADY_EXISTS = HTTPException(
        status_code=409,
        detail="Data already exists in the database.",
        headers={"WWW-Authenticate": "Bearer"},
    )
