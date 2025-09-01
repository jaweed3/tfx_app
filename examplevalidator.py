from tfx.components import ExampleValidator

def example_validator(
    stats,
    schema
):
    validator = ExampleValidator(
        statistics=stats,
        schema=schema
    )

    return validator
