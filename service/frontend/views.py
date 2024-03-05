from flask import Blueprint, render_template

blueprint = Blueprint("frontend", __name__)

@blueprint.route("/")
def index():
    return render_template("index.html")

@blueprint.route("/app.json")
def app_json():
    return {
        "name": "IoTLink Chain Faucet",
        "icon": "https://faucet.iotlinkchain.com/static/icon.png"
    }
