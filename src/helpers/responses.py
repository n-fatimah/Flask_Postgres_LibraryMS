import logging
from typing import Dict, List, Tuple, Union

from flask import jsonify


def failure_response(
    errors: Union[str, List[str]], status_code: int
) -> Tuple[Dict, int]:
    """
    Failure response function



    Args:
        errors: The error to include in the response
        status_code

    Returns:
        Tuple containing the response dictionary and HTTP status code
    """

    # logging.info(f"is: {type(errors)}")
    return {
        "status": "nok",
        "errors": [errors] if isinstance(errors, str) else errors,
    }, status_code


def success_response(data: List, status_code: int) -> Tuple[Dict, int]:
    """
    Success response function

    Args:
        data:
        status_code

    Returns:
        Tuple containing the response dictionary and HTTP status code
    """

    return {"status": "ok", "data": data}, status_code
