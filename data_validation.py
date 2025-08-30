import tensorflow_data_validation as tfdv

def validate_data(example_artifact_path):
    # Creating data statistics
    data_stats = tfdv.generate_statistics_from_tfrecord(
        data_location=example_artifact_path
    )

    # Creatting datta schema
    data_schema = tfdv.infer_schema(
        statistics=data_stats
    )
    tfdv.display_schema(schema=data_schema)

    # Validate Statistics
    anomalies = tfdv.validate_statistics(
        statistics=data_stats,
        schema=data_schema,
    )
    tfdv.display_anomalies(anomalies=anomalies)

    tfdv.get_feature(data_schema, 'URL_length').drift_comparator.infinity_norm.threshold = 0.01
    drift_anomalies = tfdv.validate_statistics(
        statistics=data_stats,
        schema=data_schema,
    )

    print(drift_anomalies)
