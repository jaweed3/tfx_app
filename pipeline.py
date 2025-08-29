from tfx.orchestration.experimental.interactive.interactive_context import InteractiveContext
from data_ingestion import example_gen

context = InteractiveContext()
context.run(example_gen)

for artifact in example_gen.outputs['examples'].get():
    print(artifact.uri)
