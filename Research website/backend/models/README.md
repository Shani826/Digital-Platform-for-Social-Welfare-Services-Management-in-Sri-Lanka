# ML Models Folder

Place your trained model files here:

## Supported formats:
- `.pkl` - Pickle files
- `.joblib` - Joblib files
- `.h5` - Keras/TensorFlow models
- `.onnx` - ONNX models

## Files to add:
1. `your_model.pkl` (or `.joblib`) - Your trained ML model
2. `encoder.pkl` (optional) - Label encoders for categorical data
3. `scaler.pkl` (optional) - Feature scalers if used

## Example:
After placing your model, update `app.py`:
```python
model = joblib.load('models/your_model.pkl')
```
