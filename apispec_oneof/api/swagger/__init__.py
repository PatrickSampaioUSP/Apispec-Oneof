import re


from apispec import APISpec
from apispec.exceptions import DuplicateComponentNameError

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_oneofschema import MarshmallowPlugin as MarshPlug

from .generator import get_schema_name, AutoDoc


class InstropectedView:
    def __init__(self, view):
        self.view = view
        self.introspectable = view["introspectable"]

    def __getattr__(self, attr):
        return self.introspectable.get(attr)


def get_uri_placeholders(uri_pattern):
    """pattern: {any}"""
    return re.findall("\{(.*?)\}", uri_pattern)


def get_spec(request, title, version, description=None, security_scheme=None):
    spec = APISpec(
        title=title,
        version=version,
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin(), MarshPlug()],
    )

    introspector = request.registry.introspector

    for view in introspector.get_category("views"):
        intro = InstropectedView(view)
        show_apispec = intro.swaggermarsh_show or False

        if not all((show_apispec, intro.request_methods)):
            continue

        # Check option before skip
        if intro.request_methods.lower() in ["head", "option"]:
            continue

        if intro.swaggermarsh_request:
            for _, v in intro.swaggermarsh_request.items():
                try:
                    spec.components.schema(get_schema_name(v), schema=v)
                except DuplicateComponentNameError:
                    pass

        if intro.swaggermarsh_responses:
            for _, v in intro.swaggermarsh_responses.items():
                try:
                    spec.components.schema(get_schema_name(v), schema=v)
                except DuplicateComponentNameError:
                    pass

        route = introspector.get("routes", intro.route_name)
        original_pattern = route["pattern"]

        autodoc = AutoDoc(
            method=intro.request_methods,
            introspectable_view=intro.introspectable,
            cornice_service=request.registry.cornice_services.get(original_pattern),
        )

        path_parameters = get_uri_placeholders(original_pattern)
        if path_parameters:
            autodoc.add_path_parameter(path_parameters)

        _op = autodoc.to_dict()

        spec.path(path="/" + original_pattern, operations=_op)

    if security_scheme:
        for k, v in security_scheme.items():
            spec.components.security_scheme(k, v)

    openapi_spec = spec.to_dict()

    if description:
        openapi_spec["info"].update({"description": description})

    scheme = request.scheme  # Or force to https
    main_server_url = "{}://{}".format(scheme, request.host)
    openapi_spec.update({"servers": [{"url": main_server_url}]})

    return openapi_spec
