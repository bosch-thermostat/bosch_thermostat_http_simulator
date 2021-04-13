import click
import logging
from flask import Flask, jsonify, abort, Response, request
from .encryption import Encryption
from .bosch_scan import BoschScan
from .const import (
    VALUE,
    NEFIT,
    IVT,
    EASYCONTROL,
    MAGICS,
)
import json
from functools import wraps
from waitress import serve

_LOGGER = logging.getLogger(__name__)


@click.group(invoke_without_command=True)
@click.option(
    "--token",
    envvar="BOSCH_ACCESS_TOKEN",
    type=str,
    default="ABCdEFGHIJHKL2MN",
    required=True,
    help="Token you want to set Default: ABCdEFGHIJHKL2MN",
)
@click.option(
    "--password",
    envvar="BOSCH_PASSWORD",
    type=str,
    default="abcdef12",
    help="Password you want to set. Default: abcdef12",
)
@click.option("-f", "--file", type=str, required=True, help="File to load")
@click.option(
    "-d",
    "--device",
    envvar="BOSCH_DEVICE",
    type=click.Choice([NEFIT, IVT, EASYCONTROL], case_sensitive=False),
    required=True,
    help="Bosch device type. NEFIT, IVT or EASYCONTROL.",
)
@click.pass_context
def cli(ctx, token: str, password: str, file: str, device: str):
    """A tool to run as Bosch thermostat simlator."""
    logging.basicConfig(level=logging.DEBUG)
    _LOGGER.info("Running Bosch simulator with:")
    _LOGGER.info("Token: %s", token)
    _LOGGER.info("Password: %s", password)
    _LOGGER.info("Device type %s", device)
    app = create_app(token, password, file, device)
    serve(app, host="0.0.0.0", port=8080)


def create_app(token, password, file, device):
    app = Flask(__name__)

    encryption = Encryption(access_key=token, magic=MAGICS[device], password=password)
    bosch_scan = BoschScan(file)

    @app.route("/<path:bosch_path>", methods=["get"])
    def index(bosch_path):
        resp = bosch_scan.get_response(bosch_path)
        if not resp:
            abort(404, description="Resource not found")
        _LOGGER.info("Returning JSON: %s", resp)
        encrypted_json = encryption.encrypt(resp)
        return Response(encrypted_json, mimetype="application/json")

    @app.route("/<path:bosch_path>", methods=["put"])
    def indexPUT(bosch_path):
        if not request.data:
            abort(404, description="No value to set")
        value_json = encryption.json_decrypt(request.data)
        new_value = value_json.get(VALUE)
        bosch_scan.update_value(bosch_path, new_value)
        _LOGGER.info("Updated value %s with %s", bosch_path, new_value)
        return ("", 204)

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({}), 404

    return app
