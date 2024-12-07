
from http import HTTPStatus
from typing import Dict, Tuple

from flask_restx import Resource

from api.role import schemas
from helpers.api import auth
from helpers.responses import failure_response, success_response
from model.role import Role

from . import api


@api.route("/create")
class CreateRole(Resource):
    @api.doc("create role")
    @api.expect(schemas.role_expect, validate=True)
    @api.marshal_list_with(schemas.role_response, skip_none=True)
    def post(self) -> Tuple[Dict, int]:
        """
        Create Role

        Returns:
            Role
        """
        api.logger.info("Create Role")
        role = Role.get_by_name(api.payload["name"])
        if role:
            err="Role already exists."
            return failure_response(err, HTTPStatus.BAD_REQUEST)

        role = Role(**api.payload).insert()
        return success_response(role, HTTPStatus.CREATED)
