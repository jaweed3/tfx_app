import tensorflow_transform as tft
from tfx.components import Transform

def transform_data(
    example_gen,
    schema_gen,
    module_file: str
):
    transformed_data = Transform(
        examples=example_gen,
        schema=schema_gen,
        module_file=module_file
    )

    return transformed_data

def preprocessing_fn(
    inputs
):
    outputs = {}

    outputs['URL_Length'] = tft.scale_to_z_score(inputs['URL_Length'])
    outputs['Result'] = inputs['Result']

    return outputs
