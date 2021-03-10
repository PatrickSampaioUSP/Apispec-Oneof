import marshmallow
from marshmallow_oneofschema import OneOfSchema


class PersonSchema(marshmallow.Schema):
    cpf = marshmallow.fields.String(required=True)
    type = marshmallow.fields.String(
        required=True, doc_default="type: person"
    )


class CompanySchema(marshmallow.Schema):
    cnpj = marshmallow.fields.String(required=True)
    type = marshmallow.fields.String(
        required=True, doc_default="type: company"
    )


class BorrowerSchema(OneOfSchema):
    type_schemas = {"company": CompanySchema, "person": PersonSchema}
    type_field = "type"


class BaseLoanRequestSchema(marshmallow.Schema):
    uuid = marshmallow.fields.UUID(dump_only=True)
    borrower = marshmallow.fields.Nested(BorrowerSchema)

    requestor = marshmallow.fields.Nested(PersonSchema)