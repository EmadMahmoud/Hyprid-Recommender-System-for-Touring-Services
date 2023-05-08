from flask import Flask
from flask_smorest import Api
from resources.endpoints import blp

app = Flask(__name__)


# flask-smorest and Blueprint configuration
app.config["API_TITLE"] = "Recommendations Endpoints"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
api.register_blueprint(blp)


