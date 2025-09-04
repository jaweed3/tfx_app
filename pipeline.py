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
    print(f"\nExample Gen Output : \n {example_gen.outputs}")
    
    # ValidationGen Component
    validate_gen = statistics_gen(example_gen.outputs['examples'])
    print(f"\nValidation Gen Output : \n {validate_gen.outputs}")

    # SchemaGen Component
    schema_data = schema_gen(validate_gen.outputs['statistics'])
    print(f"\nSchema Gen Output : \n {schema_data.outputs}")

    # Example Validator Component
    validator_data = example_validator(
        validate_gen.outputs['statistics'],
        schema_data.outputs['schema']
    ) 
    print(f"\nExample Validator Output : \n{validator_data.outputs}")

    # Transform Components
    transform = transform_data(
        example_gen=example_gen.outputs['examples'],
        schema_gen=schema_data.outputs['schema'],
        module_file=os.path.join(os.getcwd(), "transform.py")
    )
    print(f"\nTransform Components Output : \n{transform.outputs}")

    trainer = Trainer(
        module_file=os.path.join(os.getcwd(), "trainer.py"),
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        train_args=TrainArgs(splits=['train'], num_steps=10000),
        eval_args=EvalArgs(splits=['eval'], num_steps=5000)
    )
    print(f"\nTrainer Component Output : \n{trainer.outputs}")
    
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
    pipeline_root = os.path.join(os.getcwd(), 'tfx_pipeline', "pipeline")
    metadata_path = os.path.join(os.getcwd(), 'tfx_pipeline', "metadata.sqlite")

    pipeline = create_pipeline(pipeline_root, metadata_path, data_root)
    LocalDagRunner().run(pipeline)
