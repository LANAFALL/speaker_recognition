import librosa
import numpy as np
from tensorflow import load_model

# Load the model
model = load_model('my_model.keras')  # Replace 'my_model.keras' with the path to your model file

# Function to extract MFCC features from audio file
def extract_features(file_path, num_mfcc=13):
    try:
        # Load audio file with librosa
        audio, sr = librosa.load(file_path, sr=None)
        
        # Extract MFCC features
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)
        
        # Normalize MFCCs
        mfccs_processed = np.mean(mfccs.T, axis=0)
        
    except Exception as e:
        print("Error encountered while parsing file: ", file_path)
        return None
    
    return mfccs_processed

# Path to your prepared speaker audio file
audio_file_path = 'path/to/your/audio/file.wav'

# Extract features from the audio file
features = extract_features(audio_file_path)

if features is not None:
    # Reshape the features to match the model's input shape
    features = np.expand_dims(features, axis=0)  # Add a batch dimension

    # Make predictions using the model
    prediction = model.predict(features)

    # Example: Printing the prediction result
    print("Prediction:", prediction)
else:
    print("Audio file parsing failed.")
