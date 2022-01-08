from src.api.routes.v1 import v1


def register_routes(app):
    app.register_blueprint(v1)
