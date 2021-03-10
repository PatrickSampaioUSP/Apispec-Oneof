from json import JSONEncoder

import marshmallow
from pyramid.renderers import JSON

from singledispatch import singledispatch


@singledispatch
def make_data_serializable(item):
    """Convert all data's items that are non serializable to a serializable version, keeping the original data type."""
    return item


class SmarterJSONEncoder(JSONEncoder):
    def default(self, o):
        serialized_data = make_data_serializable(o)

        if serialized_data is o:  # there is no handler registered
            return super(SmarterJSONEncoder, self).default(o)

        return serialized_data


class JsonApi(JSON):
    """Custom renderer which serializes data using the proper schema.

    The schema used to dump data must be specified in the view configuration
    provided by cornice. The 'swaggermarsh_responses' argument receives a dict
    which maps the status code with the proper marshmallow schema.
    """

    @staticmethod
    def _get_schema(request):
        status_code = request.response.status_code

        try:
            # TODO (Guilherme): review the predicate name "swaggermarsh_responses".
            #  See discussion on https://github.com/geru-br/geru-loans-request/pull/871/files#r553281506
            response_schemas = request.cornice_args[0]["swaggermarsh_responses"]
        except KeyError:
            view_name = request.current_service.name
            raise Exception

        schema = response_schemas[status_code]
        return schema

    def __call__(self, info):
        def _render(obj, system):

            request = system.get("request")

            schema = self._get_schema(request)

            if not isinstance(schema, marshmallow.Schema):
                schema = schema()

            if request is not None:
                response = request.response
                response.content_type = "application/json"

            if schema.many:
                # TODO (Guilherme): adjust this code with pagination.
                return schema.dumps(obj or [], many=True, cls=SmarterJSONEncoder).data

            return schema.dumps(obj, cls=SmarterJSONEncoder).data

        return _render


schema_renderer = JsonApi()
