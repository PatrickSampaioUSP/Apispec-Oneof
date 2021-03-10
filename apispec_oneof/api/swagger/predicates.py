import sys

__all__ = [
    "SwaggerResponseSchemasPredicate",
    "SwaggerRequestSchemasPredicate",
    "SwaggerTagsPredicate",
    "SwaggerSummaryPredicate",
    "SwaggerDescriptionPredicate",
    "SwaggerSecurityPredicate",
    "SwaggerShowInPredicate",
]


class _BaseSwaggerSchemasPredicate:
    PRED_ID = "swaggermarsh"

    def __init__(self, val, _):
        self.val = val

    def text(self):
        return "{} = {}".format(self.PRED_ID, self.val)

    phash = text

    def __call__(self, context, request):
        return True


class SwaggerResponseSchemasPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_responses"


class SwaggerRequestSchemasPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_request"


class SwaggerTagsPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_tags"


class SwaggerSummaryPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_summary"


class SwaggerDescriptionPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_description"


class SwaggerSecurityPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_security"


class SwaggerShowInPredicate(_BaseSwaggerSchemasPredicate):
    PRED_ID = "swaggermarsh_show"


def register(config):
    this = sys.modules[__name__]

    for c in __all__:
        cls_ = getattr(this, c)
        config.add_view_predicate(cls_.PRED_ID, cls_)
