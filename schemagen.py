from tfx.components import SchemaGen

# Create Schema Gen function Components
def schema_gen(
    stats
):
    data_schema = SchemaGen(
        stats
    )

    return data_schema
