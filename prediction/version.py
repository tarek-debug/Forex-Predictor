from tensorflow import keras

# Correct relative path from the script's location
model = keras.models.load_model('prediction_models/CNY_to_EUR.keras')

# Print the Keras version used to build the model
print("Keras version used to build the model:", model.keras_version)
