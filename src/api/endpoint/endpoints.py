import hashlib
import logging
from http import HTTPStatus
from typing import Dict, Tuple

from flask import g, jsonify, request
from flask_restx import Resource

from api.endpoint import schemas
from helpers.api import auth
from helpers.responses import failure_response, success_response
from model.endpoint import Endpoint

from . import api


@api.route("/add")
class CreateRole(Resource):
    @api.doc("Add endpoint")
    @api.expect(schemas.endpoint_expect, validate=True)
    @api.marshal_list_with(schemas.endpoint_response, skip_none=True)
    def post(self) -> Tuple[Dict, int]:
        """
        Add endpoint

        Returns:
            Endpoint
        """
        api.logger.info("Add endpoint")
        endpoint = Endpoint.get_by_route_method(
            api.payload["route"], api.payload["method"]
        )
        if endpoint:
            return failure_response(
                ["Endpoint already exists."], HTTPStatus.BAD_REQUEST
            )

        endpoint = Endpoint(**api.payload).insert()
        return success_response(endpoint, HTTPStatus.CREATED)
