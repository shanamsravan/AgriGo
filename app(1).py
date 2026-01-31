from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample fertilizer recommendations based on crop type
FERTILIZER_DATA = {
    "Wheat": {"Nitrogen": 120, "Phosphorus": 60, "Potassium": 40},
    "Rice": {"Nitrogen": 150, "Phosphorus": 80, "Potassium": 50},
    "Corn": {"Nitrogen": 180, "Phosphorus": 90, "Potassium": 60},
    "Soybean": {"Nitrogen": 100, "Phosphorus": 50, "Potassium": 30},
    "Barley": {"Nitrogen": 110, "Phosphorus": 55, "Potassium": 35},
    "Potato": {"Nitrogen": 140, "Phosphorus": 70, "Potassium": 45},
    "Tomato": {"Nitrogen": 130, "Phosphorus": 65, "Potassium": 40},
    "Sugarcane": {"Nitrogen": 200, "Phosphorus": 100, "Potassium": 70}
}

@app.route('/recommend_fertilizer', methods=['POST'])
def recommend_fertilizer():
    try:
        data = request.get_json()
        crop_type = data.get("crop_type", "").strip()

        if not crop_type:
            return jsonify({"error": "Crop type is required."}), 400

        recommendations = FERTILIZER_DATA.get(crop_type)

        if recommendations is None:
            return jsonify({"error": f"No fertilizer recommendations found for '{crop_type}'."}), 404

        # Get the highest required nutrient as the primary recommendation
        primary_fertilizer, amount = max(recommendations.items(), key=lambda x: x[1])

        return jsonify({
            "crop_type": crop_type,
            "recommended_fertilizer": {
                "type": primary_fertilizer,
                "amount_kg_per_hectare": amount
            }
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
