from webargs.flaskparser import use_args
from datetime import datetime, timedelta
from ..clients import Bitcoin
from .args import faucet_args
from flask import Blueprint, request
from ..abort import abort
from pony import orm
import config

from ..models import Request

blueprint = Blueprint("api", __name__, url_prefix="/api")

@blueprint.route("/faucet", methods=["POST"])
@use_args(faucet_args, location="json")
@orm.db_session
def faucet(args):
    result = {"error": None, "data": {}}
    client = Bitcoin(config.endpoint)
    address = args["address"]

    # Split message for validation
    data = args["message"].split("/")

    # Make sure message consists of prefix and timestamp
    if len(data) != 2:
        return abort("faucet", "invalid-message")

    # Validate prefix
    if data[0] != config.auth_prefix:
        return abort("faucet", "invalid-prefix")

    # Make sure timestamp is a number
    if not data[1].isdigit():
        return abort("faucet", "invalid-timestamp")

    time = datetime.fromtimestamp(int(data[1]))
    now = datetime.utcnow()

    start = now - timedelta(
        minutes=now.minute % config.auth_minutes,
        seconds=now.second,
        microseconds=now.microsecond
    )

    until = start + timedelta(minutes=config.auth_minutes)

    if time > until or time < start:
        return abort("faucet", "invalid-timestamp")

    # Verify user signed message
    verify = client.make_request("verifymessage", [
        address, args["signature"], args["message"]
    ])

    if verify["error"] or not verify["result"]:
        return abort("faucet", "invalid-signature")

    
    user_agent = request.user_agent.string
    user_agent = user_agent if user_agent else "Missing Agent"
    ip = request.remote_addr

    if (faucet_request := Request.select(lambda r: r.address == address).first()):
        if faucet_request.created > datetime.utcnow() - timedelta(days=1):
            return abort("faucet", "try-later")

    if (faucet_request := Request.select(lambda r: r.ip == ip).first()):
        if faucet_request.created > datetime.utcnow() - timedelta(days=1):
            return abort("faucet", "try-later")

    faucet_request = Request(**{
        "amount": config.faucet_amount,
        "agent": user_agent,
        "address": address,
        "ip": ip
    })

    result["data"] = {
        "amount": float(faucet_request.amount),
        "token": config.faucet_token
    }

    return result

@blueprint.route("/time", methods=["GET"])
@orm.db_session
def server_time():
    now = datetime.utcnow()

    start = now - timedelta(
        minutes=now.minute % config.auth_minutes,
        seconds=now.second,
        microseconds=now.microsecond
    )

    until = start + timedelta(minutes=config.auth_minutes)

    return {"error": None, "data": {
        "until": int(until.timestamp()),
        "time": int(now.timestamp()),
        "prefix": config.auth_prefix
    }}

@blueprint.route("/me", methods=["GET"])
def user_info():
    user_agent = request.user_agent.string
    user_agent = user_agent if user_agent else "Missing Agent"
    ip = request.remote_addr

    return {"error": None, "data": {
        "agent": user_agent,
        "ip": ip
    }}
