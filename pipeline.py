from tfx.components import Trainer
from tfx.orchestration import metadata
from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.orchestration.pipeline import Pipeline
from tfx.v1.proto import TrainArgs, EvalArgs
from examplegen import examplegen
from schemagen import schema_gen
from statisticsgen import statistics_gen
from examplevalidator import example_validator
from transform import transform_data
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

    # Transform Components
    transform = transform_data(
        example_gen=example_gen.outputs['examples'],
        schema_gen=schema_data.outputs['schema'],
        module_file=os.path.join(os.getcwd(), "transform.py")
    )
    print(f"\nTransform Components : \n{transform}")

    trainer = Trainer(
        module_file=os.path.join(os.getcwd(), "trainer.py"),
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        train_args=TrainArgs(splits=['train'], num_steps=10000),
        eval_args=EvalArgs(splits=['eval'], num_steps=5000)
    )
    print(f"\nTrainer Component : \n{trainer}")
    
    components = [
        example_gen,
        validate_gen,
        schema_data,
        validator_data,
        transform,
        trainer
    ]

    return Pipeline(
        pipeline_name="phishing_pipeline",
        pipeline_root=pipeline_root,
        metadata_connection_config=metadata.sqlite_metadata_connection_config(metadata_path),
        components=components
    ) 

if __name__ == "__main__":
    pipeline_root = os.path.join(data_root, "pipeline")
    metadata_path = os.path.join(data_root, "metadata.sqlite")

    pipeline = create_pipeline(pipeline_root, metadata_path, data_root)
    LocalDagRunner().run(pipeline)
