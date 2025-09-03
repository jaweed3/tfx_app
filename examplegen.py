import tensorflow as tf
import os
from tfx.proto import example_gen_pb2
from tfx.components import CsvExampleGen
from tfx.v1.dsl import Importer
import glob

FILE_NAME = 'phisingData_utf8.csv'
base_dir = os.getcwd()
data_dir = os.path.join(base_dir, 'data')
file_path = os.path.join(base_dir, FILE_NAME)

def examplegen(data_dir):
    output = example_gen_pb2.Output(
       split_config=example_gen_pb2.SplitConfig(splits=[
            example_gen_pb2.SplitConfig.Split(name='train', hash_buckets=6),
            example_gen_pb2.SplitConfig.Split(name='eval', hash_buckets=2),
            example_gen_pb2.SplitConfig.Split(name='test', hash_buckets=2)
        ]) 
    )
    
    print("🔎 Checking CSV files in input_base:")
    print(glob.glob(os.path.join(data_dir, "*.csv")))
    
    with open(os.path.join(data_dir, "phisingData.csv"), "rb") as f:
        raw_bytes = f.read(200)
        print("🔎 First 200 raw bytes:", raw_bytes)
    
    with open(os.path.join(data_dir, "phisingData.csv"), "r", errors="replace") as f:
        head = [next(f) for _ in range(5)]
        print("🔎 First 5 lines (with replacement for bad chars):")
        print(head)
  
    return CsvExampleGen(
        input_base=data_dir, 
        output_config=output)

if __name__ == "__main__":
    example_gen = examplegen(data_dir=data_dir)
    print(example_gen)
