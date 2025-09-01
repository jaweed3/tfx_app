from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.orchestration.pipeline import Pipeline
from tfx_bsl.coders import example_coder
from examplegen import examplegen
from schemagen import schema_gen
from statisticsgen import statistics_gen
from examplevalidator import example_validator
import os

data_root = os.path.join(os.getcwd(), 'data')

def create_pipeline(pipeline_root, metadata_path, data_root):
    # ExmapleGen Components
    example_gen = examplegen(data_root)
    print(f"\nExample Gen : \n {example_gen}")
    
    # ValidationGen Component
    validate_gen = statistics_gen(example_gen.outputs['examples'])
    print(f"\nValidation Gen : \n {validate_gen}")

    # SchemaGen Component
    schema_data = schema_gen(validate_gen.outputs['statistics'])
    print(f"\nSchema Gen : \n {schema_data}")

    # Example Validator Component
    validator_data = example_validator(
        validate_gen.outputs['statistics'],
        schema_data.outputs['schema']
    ) 
    print(f"\nExample Validator : \n{validator_data}")

    components = [
        example_gen,
        validate_gen,
        schema_data,
        validator_data
    ]

    return Pipeline(
        pipeline_name="phishing_pipeline",
        pipeline_root=pipeline_root,
        metadata_connection_config=None,
        components=components
    ) 

if __name__ == "__main__":
    pipeline_root = os.path.join(data_root, "pipeline")
    metadata_path = os.path.join(data_root, "metadata")

    pipeline = create_pipeline(pipeline_root, metadata_path, data_root)
