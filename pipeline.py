from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.orchestration.pipeline import Pipeline
from tfx_bsl.coders import example_coder
from data_ingestion import create_ingestion
from data_validation import validate_data
import os

data_root = os.path.join(os.getcwd(), 'data')

def create_pipeline(pipeline_root, metadata_path, data_root):
    # ExmapleGen Components
    example_gen = create_ingestion(data_root)
    
    # ValidationGen Component
    validate_gen = validate_data(example_gen.outputs['examples'])

    components = [
        example_gen,
        validate_gen
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
    print(pipeline)
