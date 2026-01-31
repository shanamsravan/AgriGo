@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('home'))  # Ensure user is logged in
    
    crop = request.form['crop']
    symptoms = request.form['symptoms']
    
    # Your prediction logic here (e.g., machine learning model)
    # Let's assume the prediction is based on some conditions
    prediction = "No disease detected"  # Placeholder
    
    return render_template('prediction.html', prediction=prediction)
