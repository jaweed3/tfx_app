from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.orchestration.pipeline import Pipeline
from data_ingestion import create_ingestion
import os



data_root = os.path.join(os.getcwd(), 'data')
example_gen = create_ingestion(data_root)

def create_pipeline(pipeline_root, metadata_path, data_root):
    example_gen = create_ingestion(data_root)

    return Pipeline(
        pipeline_name="phishing_pipeline",
        pipeline_root=pipeline_root,
        metadata_connection_config=None,
        components=[
            example_gen
        ]
    ) 

if __name__ == "__main__":
    pipeline_root = os.path.join(data_root, "pipeline")
    metadata_path = os.path.join(data_root, "metadata")

    pipeline = create_pipeline(pipeline_root, metadata_path, data_root)
    print(pipeline)
