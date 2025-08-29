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

# Comparing dataset's statistics
train_stats = tfdv.generate_statistics_from_csv(
    data_location='/data/train/001.csv',
    delimiter=','
)
val_stats = tfdv.generate_statistics_from_csv(
    data_location='/data/train/001.csv',
    delimiter=','
)

# Visualize the comparison between those two
tfdv.visualize_statistics(lhs_statistics=val_stats, rhs_statistics=train_stats,
                          lhs_name='VAL_DATASET', rhs_name='TRAIN_DATASET')

# Detect the Anomaly wih TFDV
anomalies = tfdv.validate_statistics(statistics=val_stats, schema=schema)

try: 
    tfdv.display_anomalies(anomalies)
except:
    print("Error Occured")

print(anomalies)

tfdv.get_feature(schema, 'URL_length').drift_comparator.infinity_norm.threshold = 0.01
drift_anomalies = tfdv.
