import numpy as np
from keras_preprocessing.sequence import pad_sequences
import tensorflow as tf
import pickle
import os
from database import db_controller

# Suppress TensorFlow warnings as requested in logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Import layers for robust custom_objects mapping
from tensorflow.keras.layers import GRU, Bidirectional, Embedding

controller = db_controller.db_controller()

class S_model:
    def __init__(self):
        # Load model with comprehensive custom_objects to handle nested layers (Bidirectional -> GRU)
        # compile=False avoids errors with legacy optimizers in Keras 3
        custom_mapping = {
            'GRU': GRU,
            'Bidirectional': Bidirectional,
            'Embedding': Embedding
        }
        
        try:
            self.model = tf.keras.models.load_model(
                'my_model.h5', 
                custom_objects=custom_mapping,
                compile=False
            )
            print("Sentiment model (GRU) loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback for alternative Keras internal names
            self.model = tf.keras.models.load_model(
                'my_model.h5', 
                custom_objects=custom_mapping,
                compile=False,
                safe_mode=False
            )
            
        # Load Tokenizer from the current directory
        try:
            with open('tokenizer.pickle', 'rb') as handle:
                self.loaded_tokenizer = pickle.load(handle)
                print("Tokenizer loaded successfully.")
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            
    def predict(self, message):
        if not hasattr(self, 'loaded_tokenizer') or self.model is None:
            print("Model or Tokenizer not initialized.")
            return [0.0] * 6 # Default neutral-ish scores
            
        msg = [message]
        seq = self.loaded_tokenizer.texts_to_sequences(msg)
        padded = pad_sequences(seq, maxlen=500)
        pred = self.model.predict(padded)
        return pred[0]
        
    def get_sentiment_label(self, pred):
        if pred[np.argmax(pred)] > 0.65:
            return ['anger', 'sadness', 'fear', 'joy', 'surprise', 'love'][np.argmax(pred)]
        else:
            return 'neutral'
