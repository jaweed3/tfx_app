import absl
import tensorflow as tf
import tensorflow_transform as tft
from tf.keras.layers import Input, Dense, concatenate
from tfx.components import Trainer, CsvExampleGen
from tfx.v1.proto import TrainArgs, EvalArgs
from tfx.components.trainer.fn_args_utils import FnArgs

def training_phase(
    module_file,
    examples,
    transform_graph,
    train_steps,
    eval_steps
):
    trainer = Trainer(
        module_file=module_file,
        examples=examples,
        transform_graph=transform_graph,
        train_args=TrainArgs(splits=['train'], num_steps=train_steps),
        eval_args=EvalArgs(splits=['eval'], num_steps=eval_steps)
    )

def _build_keras_model(
    transform_output: tft.TFTransformOutput) -> tf.keras.Model :
    feature_spec = transform_output.transformed_feature_spec().copy()
    feature_spec.pop('Result')

    inputs = {}
    for key, items in feature_spec.items():
        inputs[key] = Input(shape=spec.shape, name=key, dtype=spec.dtype)

    # Combine add features
    concatenate_features = concatenate(list(inputs.values())) 

    x = Dense(8, activation='relu')(concatenate_features)
    x = Dense(8, activation='relu')(x)

    output_layer = Dense(3)(x)

    model = tf.keras.Model(
        inputs=inputs, 
        outputs=output_layer)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    model.summary(print_fn=absl.logging.info)

    return model

# Reading Transformed Data from TFX
def _input_fn(
        file_pattern: str,
        tf_transform_output : tft.TFTransformOutput,
        batch_size: int = 32) -> tf.data.Dataset:
    """
    Create Dataset for training and evaluation
    """
    dataset = 

def run_fn(
    train_data: CsvExampleGen,
    eval_data: CsvExampleGen,
    fn_args: FnArgs) -> None:

    # Define train dataset
    train_dataset = train_data

    # Define Eval Dataset
    eval_dataset = eval_data

    #
    model = _build_keras_model()

    model.fit()
    model.save(fn_args.serving_model_dir)
