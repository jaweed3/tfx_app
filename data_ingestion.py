import tensorflow as tf
import os
from tfx.proto import example_gen_pb2
from tfx.components import CsvExampleGen
from tfx.v1.dsl import Importer

FILE_NAME = 'phisingData.csv'
base_dir = os.getcwd()
file_path = os.path.join(data_dir, FILE_NAME)
output = example_gen_pb2.Output(
   split_config=example_gen_pb2.SplitConfig(splits=[
        example_gen_pb2.SplitConfig.Split(name='train', hash_buckets=6),
        example_gen_pb2.SplitConfig.Split(name='eval', hash_buckets=2),
        example_gen_pb2.SplitConfig.Split(name='test', hash_buckets=2)
    ]) 
)

example_gen = CsvExampleGen(input_base=file_path, output_config=output)
