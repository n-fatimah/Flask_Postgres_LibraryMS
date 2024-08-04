import hashlib
import logging
from http import HTTPStatus
from typing import Dict, Tuple

from flask import g, jsonify, request
from flask_restx import Resource

from api.user import schemas
from helpers.api import auth
from helpers.auth import generate_jwt
from helpers.responses import failure_response, success_response
from model.user import User

from . import api


@api.route("/signup")
class SignUp(Resource):
    @api.doc("Sign Up")
    @api.expect(schemas.user_expect, validate=True)
    @api.marshal_list_with(schemas.user_response, skip_none=True)
    @auth("/user/signup")
    def post(self) -> Tuple[Dict, int]:
        """
        Sign Up

        Returns:
            User
        """
        api.logger.info("Create user")
        user = User.get_by_email(api.payload["email"])
        if user:
            return failure_response(["Cannot add a user."], HTTPStatus.BAD_REQUEST)

        hashed_password = hashlib.sha256(api.payload["password"].encode()).hexdigest()
        api.payload["password"] = hashed_password
        role_id = user.role_id

        token = generate_jwt(user.id, role_id)
        logging.info(f"token: {token}")
        user = User(**api.payload).insert()

        return success_response(user, HTTPStatus.CREATED)


@api.route("/login")
class Login(Resource):
    @api.doc("User login")
    @api.expect(schemas.user_login_expect, validate=True)
    @api.marshal_list_with(schemas.user_response, skip_none=True)
    @auth("/user/login")
    def post(self):
        """
        Authenticate user and return JWT token

        Returns:
            JWT token
        """
        api.logger.info("User login")
        email = api.payload["email"]
        password = api.payload["password"]

        user = User.get_by_email(email)
        if not user or not user.check_password(user.password, password):
            return failure_response(
                ["Invalid email or password."], HTTPStatus.UNAUTHORIZED
            )

        role_id = user.role_id
        token = generate_jwt(user.id, role_id)
        logging.info(f"token: {token}")

        return success_response(user, HTTPStatus.OK)


@api.route("/list")
class UserList(Resource):
    @api.doc("List users")
    @api.param("page")
    @api.param("per_page")
    @api.marshal_list_with(schemas.user_list_response, skip_none=True)
    @auth("/user/list")
    def get(self) -> Tuple[Dict, int]:
        """
        Get all users

        Returns:
            List of users
        """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=4, type=int)
        api.logger.info("List users")
        users = User.list(page=page, per_page=per_page)

        return success_response(users, HTTPStatus.OK)


@api.route("/<int:user_id>")
class UserItem(Resource):
    @api.doc("Get user by id")
    @api.marshal_list_with(schemas.user_response, skip_none=True)
    def get(self, user_id: int) -> Tuple[Dict, int]:
        """
        Get user by id

        Args:
            user_id: user id

        Returns:
            User
        """
        api.logger.info(f"Get a users with ID: {user_id}")
        user = User.get_by_id(user_id)
        if not user:
            return failure_response(["User does not exist."], HTTPStatus.NOT_FOUND)
        return success_response(user, HTTPStatus.OK)

    @api.doc("Delete user")
    @auth
    def delete(self, user_id: int) -> Tuple[dict, int]:
        """
        Delete user
        An authenticated user can delete any other user

        Returns:
            Failure or 204
        """
        api.logger.info("Delete user")
        user = User.get_by_id(user_id)
        if not user:
            return failure_response(["User does not exist."], HTTPStatus.NOT_FOUND)
        logging.info(g.user.email, " is deleting ", user.email)
        user.delete()
        return success_response(user, HTTPStatus.OK)
