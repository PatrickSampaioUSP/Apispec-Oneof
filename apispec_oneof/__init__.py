from pyramid.config import Configurator


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)

    config.include("pyramid_apispec.views")
    config.include("cornice")
    config.include(".api")
    config.add_route("health", "/health")

    return config.make_wsgi_app()
