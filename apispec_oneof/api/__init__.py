from apispec_oneof.api.swagger import predicates
from apispec_oneof.api.swagger.apispecview import api_spec
from apispec_oneof.api.swagger.renderers import schema_renderer


def includeme(config):
    predicates.register(config)
    config.scan(".views")

    config.add_renderer(None, schema_renderer)
    config.add_route("openapi_spec", "/openapi.json")
    config.add_view(api_spec, route_name="openapi_spec", renderer="json")

    config.pyramid_apispec_add_explorer(
        spec_route_name="openapi_spec",
        explorer_route_path="/api-explorer",
    )
