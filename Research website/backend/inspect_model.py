import joblib
import pickle

# Load and inspect the model
print("=" * 50)
print("INSPECTING MODEL")
print("=" * 50)

try:
    model = joblib.load('models/welfare_model.pkl')
    print(f"Model type: {type(model)}")
    print(f"Model: {model}")
    
    # Try to get feature names if available
    if hasattr(model, 'feature_names_in_'):
        print(f"\nFeature names: {model.feature_names_in_}")
    if hasattr(model, 'n_features_in_'):
        print(f"Number of features: {model.n_features_in_}")
    if hasattr(model, 'classes_'):
        print(f"Classes/Output labels: {model.classes_}")
except Exception as e:
    print(f"Error loading model with joblib: {e}")
    try:
        with open('models/welfare_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print(f"Model type: {type(model)}")
        print(f"Model: {model}")
    except Exception as e2:
        print(f"Error loading model with pickle: {e2}")

print("\n" + "=" * 50)
print("INSPECTING LABEL ENCODER")
print("=" * 50)

try:
    encoder = joblib.load('models/label_encoder.pkl')
    print(f"Encoder type: {type(encoder)}")
    
    if isinstance(encoder, dict):
        print("Encoder is a dictionary with keys:")
        for key, val in encoder.items():
            print(f"  - {key}: {type(val)}")
            if hasattr(val, 'classes_'):
                print(f"      Classes: {val.classes_[:10]}...")  # First 10
    elif hasattr(encoder, 'classes_'):
        print(f"Classes: {encoder.classes_}")
except Exception as e:
    print(f"Error loading encoder with joblib: {e}")
    try:
        with open('models/label_encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
        print(f"Encoder type: {type(encoder)}")
    except Exception as e2:
        print(f"Error loading encoder with pickle: {e2}")
