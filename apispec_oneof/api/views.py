from cornice import Service
from cornice.validators import marshmallow_body_validator

from apispec_oneof.api.schemas import BaseLoanRequestSchema

storage_v1 = Service(name="storage_v1", path="/state/{session}")


@storage_v1.put(
    permission="edit",
    content_type="application/json",
    swaggermarsh_tags=["My Resource"],
    swaggermarsh_summary="API summary",
    swaggermarsh_description="""
    More detailed description.
    """,
    validators=(marshmallow_body_validator,),
    swaggermarsh_request=dict(body=BaseLoanRequestSchema),
    swaggermarsh_show=True,
)  # pylint: disable=E1101
def set_state(request):
    pass
