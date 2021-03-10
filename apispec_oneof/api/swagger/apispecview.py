from apispec_oneof.api.swagger import get_spec


def api_spec(request):
    return get_spec(
        request=request,
        title="Swagger Poc",
        version="4.0.0",
        description="""
        Swagger POC of libraries.
        """,
    )
