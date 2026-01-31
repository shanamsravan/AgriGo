from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy dataset or predefined logic for prediction
crop_data = {
    "wheat": {"temperature": 25, "humidity": 60, "leaf_color": "green", "soil_type": "Loamy"},
    "rice": {"temperature": 30, "humidity": 80, "leaf_color": "green", "soil_type": "Sandy"},
    "corn": {"temperature": 22, "humidity": 70, "leaf_color": "yellow", "soil_type": "Loamy"},
    # Add other crops as needed
}

# Fertilizer recommendations for crops
fertilizer_recommendations = {
    "wheat": {"Nitrogen": 20, "Phosphorus": 10, "Potassium": 15},
    "rice": {"Nitrogen": 15, "Phosphorus": 12, "Potassium": 18},
    "corn": {"Nitrogen": 25, "Phosphorus": 8, "Potassium": 20},
    # Add other crops as needed
}

# Disease prediction logic (can be replaced with a machine learning model)
def predict_disease(crop_type):
    # Here you can implement your logic or ML model
    if crop_type == "wheat":
        return "Leaf Blight"
    elif crop_type == "rice":
        return "Rice Blast"
    elif crop_type == "corn":
        return "Corn Smut"
    else:
        return "No Disease Prediction Available"

@app.route('/predict', methods=['GET'])
def predict():
    # For now, you can take a default crop type (or pass one as a query parameter)
    crop_type = request.args.get('crop_type', 'wheat')  # Default to 'wheat'

    # Fetch data related to the crop type
    crop_info = crop_data.get(crop_type.lower(), {})
    disease = predict_disease(crop_type)

    # Get fertilizer recommendation for the crop
    fert_recommendations = fertilizer_recommendations.get(crop_type.lower(), {})

    # Prepare response
    response = {
        "disease": disease,
        "fertilizer_recommendation": fert_recommendations
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
