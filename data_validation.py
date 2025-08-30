import tensorflow_data_validation as tfdv
from tfx.components.statistics_gen.component import StatisticsGen

def validate_data(tfrecord_channel):
    # Statistics Gen
    data_stats = StatisticsGen(
        examples=tfrecord_channel
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
