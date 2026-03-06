import numpy as np
from keras_preprocessing.sequence import pad_sequences
import tensorflow as tf
import pickle
from database import db_controller

controller = db_controller.db_controller();

class S_model:
    def __init__(self):
        # Load model from the current directory
        # Using custom_objects to fix 'GRU' not found error in some Keras/TF versions
        try:
            self.model = tf.keras.models.load_model(
                'my_model.h5', 
                custom_objects={'GRU': tf.keras.layers.GRU}
            )
        except Exception as e:
            print(f"Error loading model with custom_objects: {e}")
            # Fallback for different Keras versions
            self.model = tf.keras.models.load_model('my_model.h5')
        
        # Load Tokenizer from the current directory
        with open('tokenizer.pickle', 'rb') as handle:
            self.loaded_tokenizer = pickle.load(handle)
            
    def predict(self, message):
        msg = [message,];
        seq=self.loaded_tokenizer.texts_to_sequences(msg)
        padded=pad_sequences(seq,maxlen=500)
        pred=self.model.predict(padded)
        #print(max(pred[0]))
        #print(pred[0][np.argmax(pred)])
        #print(np.argmax(pred))
        return pred[0];
        if pred[0][np.argmax(pred)] > 0.65:
            return['anger','sadness','fear','joy','surprise','love'][np.argmax(pred)];
           
        else:
            return 'neutral';
        
        