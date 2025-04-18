
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load("model.pkl")  # Ensure this file is uploaded to backend before deployment

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    # Extract features expected by the model
    features = [
        float(data["count"]),
        float(data["dst_host_diff_srv_rate"]),
        float(data["dst_host_same_src_port_rate"]),
        float(data["dst_host_same_srv_rate"]),
        float(data["dst_host_srv_count"]),
        float(data["flag"] == "SF"),  # Simplified encoding
        float(data["last_flag"]),
        float(data["logged_in"]),
        float(data["same_srv_rate"]),
        float(data["serror_rate"]),
        float(data["service_http"])
    ]

    # Make prediction
    prediction = model.predict([features])[0]
    return jsonify({"prediction": str(prediction)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
