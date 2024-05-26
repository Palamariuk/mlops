from flask import Flask, request, jsonify
import joblib
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

model_path = os.path.join(os.path.dirname(__file__), 'models/model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'models/vectorizer.pkl')

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    app.logger.info("Model and vectorizer loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading model or vectorizer: {e}")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['short_description']
        app.logger.info(f"Received data: {data}")
        if not data:
            return jsonify({'error': 'No text provided'}), 400
        vect_data = vectorizer.transform([data])
        prediction = model.predict(vect_data)
        app.logger.info(f"Prediction: {prediction[0]}")
        return jsonify({'prediction': prediction[0]}), 200
    except Exception as e:
        app.logger.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
