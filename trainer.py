from absl import logging
import tensorflow as tf
import tensorflow_transform as tft
from tensorflow.keras.layers import Input, Dense, concatenate
from tfx.components.trainer.fn_args_utils import FnArgs

# Fitur dan label
FEATURE_KEY = [
    "having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol",
    "double_slash_redirecting","Prefix_Suffix","having_Sub_Domain","SSLfinal_State",
    "Domain_registeration_length","Favicon","port","HTTPS_token","Request_URL",
    "URL_of_Anchor","Links_in_tags","SFH","Submitting_to_email","Abnormal_URL",
    "Redirect","on_mouseover","RightClick","popUpWidnow","Iframe","age_of_domain",
    "DNSRecord","web_traffic","Page_Rank","Google_Index","Links_pointing_to_page",
    "Statistical_report"
]

LABEL_KEY = "Result"

def _build_keras_model(transform_output: tft.TFTransformOutput) -> tf.keras.Model:
    """Build Keras model for training."""
    feature_spec = transform_output.transformed_feature_spec().copy()

    # Pastikan label tidak ikut diinput
    if LABEL_KEY in feature_spec:
        feature_spec.pop(LABEL_KEY)

    # Buat input layer untuk tiap fitur
    inputs = {
        key: Input(shape=spec.shape, name=key, dtype=spec.dtype)
        for key, spec in feature_spec.items()
    }

    # Gabung semua fitur
    concatenate_features = concatenate(list(inputs.values())) 

    # Hidden layers
    x = Dense(64, activation='relu')(concatenate_features)
    x = Dense(32, activation='relu')(x)

    # Output layer → Binary Classification
    output_layer = Dense(1, activation="sigmoid")(x)

    # Model
    model = tf.keras.Model(inputs=inputs, outputs=output_layer)

    # Compile
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
        metrics=[tf.keras.metrics.BinaryAccuracy(name="accuracy")]
    )

    model.summary(print_fn=logging.info)
    return model



def _input_fn(file_pattern, tf_transform_output, batch_size=32):
    print("🔎 DEBUG: File pattern received by _input_fn:", file_pattern)

    feature_spec = tf_transform_output.transformed_feature_spec()

    dataset = tf.data.experimental.make_batched_features_dataset(
        file_pattern=file_pattern,
        batch_size=batch_size,
        features=feature_spec,
        reader=tf.data.TFRecordDataset,   # pastikan pakai TFRecordDataset
        label_key=LABEL_KEY
    )

    # Peek one batch
    for x, y in dataset.take(1):
        print("✅ DEBUG: One batch of features:", list(x.keys()))
        print("✅ DEBUG: One batch of labels:", y.numpy())

    return dataset



def run_fn(fn_args: FnArgs) -> None:
    """Train and save the model."""
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

    train_dataset = _input_fn(fn_args.train_files, tf_transform_output)
    eval_dataset = _input_fn(fn_args.eval_files, tf_transform_output)

    model = _build_keras_model(tf_transform_output)

    model.fit(
        train_dataset,
        steps_per_epoch=fn_args.train_steps,
        validation_data=eval_dataset,
        validation_steps=fn_args.eval_steps
    )

    # Save for serving
    model.save(fn_args.serving_model_dir, save_format='tf')
