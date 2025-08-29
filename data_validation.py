import tensorflow_data_validation as tfdv

stats = tfdv.generate_statistics_from_csv(
    data_location='/data/phishingData.csv',
    delimiter=','
)

# Generating Schema from the dataset
schema = tfdv.infer_schema(stats)
tfdv.display_schema(schema)

# Visulaize Statistics
tfdv.visualize_statistics(stats)

