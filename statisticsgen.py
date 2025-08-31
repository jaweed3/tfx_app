import tensorflow_data_validation as tfdv
from tfx.components.statistics_gen.component import StatisticsGen

def statistics_gen(tfrecord_channel):
    # Statistics Gen
    data_stats = StatisticsGen(
        examples=tfrecord_channel
    )

    print(data_stats)

    return data_stats
