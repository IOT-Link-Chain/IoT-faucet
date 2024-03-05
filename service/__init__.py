from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from flask import Flask
from .models import db
import config

db.bind(**config.db)
db.generate_mapping(create_tables=True)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.secret
    CORS(app)

    if config.proxy_fix:
        app.wsgi_app = ProxyFix(
            app.wsgi_app, x_for=config.x_for
        )

    with app.app_context():
        from .frontend import frontend
        from .api import api

        app.register_blueprint(frontend)
        app.register_blueprint(api)

        return app
