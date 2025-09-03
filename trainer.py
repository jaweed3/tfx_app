from absl import logging
import tensorflow as tf
import tensorflow_transform as tft
from tensorflow.keras.layers import Input, Dense, concatenate
from tfx.components import Trainer
from tfx.components.trainer.fn_args_utils import FnArgs

FEATURE_KEY = ["having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol","double_slash_redirecting","Prefix_Suffix","having_Sub_Domain","SSLfinal_State","Domain_registeration_length","Favicon","port","HTTPS_token","Request_URL","URL_of_Anchor","Links_in_tags","SFH","Submitting_to_email","Abnormal_URL","Redirect","on_mouseover","RightClick","popUpWidnow","Iframe","age_of_domain","DNSRecord","web_traffic","Page_Rank","Google_Index","Links_pointing_to_page","Statistical_report"]

LABEL_KEY = ["Result"]

def _transformed_name(key) -> None:
    return key + "_xf"

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

    model.summary(print_fn=logging.info)

    return model

# Reading Transformed Data from TFX
def _input_fn(
        file_pattern: str,
        tf_transform_output : tft.TFTransformOutput,
        batch_size: int = 32) -> tf.data.Dataset:
    """
    Create Dataset for training and evaluation
    """
    dataset = tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=tf_transform_output.transformed_feature_spec(),
        reader=tf.data.TFRecordDataset,
        label_key=_transformed_name(LABEL_KEY)
    )
    return dataset

def run_fn(fn_args: FnArgs) -> None :
    """Entry Point for TFX Trainer Component"""

    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

    train_dataset = _input_fn(fn_args.train_files, tf_transform_output)
    eval_dataset = _input_fn(fn_args.eval_files,  tf_transform_output)

    model = _build_keras_model()

    model.fit(
        train_dataset,
        steps_per_epoch=fn_args.train_steps,
        validation_data=eval_dataset,
        validation_steps=fn_args.eval_steps
    )
    model.save(fn_args.serving_model_dir, save_format='tf')
