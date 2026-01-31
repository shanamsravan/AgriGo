from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change for production

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shanamsravan55@gmail.com'          # ✅ Your Gmail
app.config['MAIL_PASSWORD'] = 'chsl jazv guss ytxd'           # 🔐 App Password
app.config['MAIL_DEFAULT_SENDER'] = '23ag1a1255@gmail.com'    # ✅ Must match MAIL_USERNAME

mail = Mail(app)

# ✅ Dummy user store for testing (use real emails for testing)
users = {
    "testuser123@gmail.com": {"password": generate_password_hash("mypassword")}
}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users:
            flash("Email already registered!", "error")
            return redirect(url_for('register'))

        users[email] = {'password': generate_password_hash(password)}
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if email not in users:
        flash("You must register first!", "error")
        return redirect(url_for('register'))

    user = users.get(email)

    if user and check_password_hash(user['password'], password):
        session['email'] = email

        # ✅ Send login email to the user
        try:
            msg = Message("Login Successful", recipients=[email])
            msg.body = "You have successfully logged into the Crop Disease and Fertilizer Management System."
            msg.html = "<p>You have successfully logged into the <b>Crop Disease and Fertilizer Management System</b>.</p>"
            mail.send(msg)
            print(f"✅ Email sent to {email}")
        except Exception as e:
            print(f"❌ Email sending failed to {email}: {e}")

        flash("You have logged into the Crop Disease and Fertilizer Management System.", "success")
        return redirect(url_for('prediction_page'))
    else:
        flash("Invalid login credentials!", "error")
        return redirect(url_for('home'))

@app.route('/prediction')
def prediction_page():
    if 'email' not in session:
        return redirect(url_for('home'))
    return render_template('index.html', email=session['email'])

@app.route('/predict_disease', methods=['POST'])
def predict_disease():
    data = request.get_json()
    symptoms = data.get('symptoms', [])

    temperature = symptoms[0]
    humidity = symptoms[1]
    leaf_color = symptoms[2].lower()
    soil_type = symptoms[3].lower()

    if leaf_color == 'yellow' and soil_type == 'clay':
        disease = "Nitrogen Deficiency"
    elif float(temperature) > 35 and float(humidity) > 80:
        disease = "Fungal Infection"
    elif leaf_color in ["brown", "yellow"]:
        disease = "Leaf Spot"
    else:
        disease = "No major disease detected"

    return jsonify({"disease": disease})

@app.route('/recommend_fertilizer', methods=['POST'])
def recommend_fertilizer():
    data = request.get_json()
    crop_type = data.get('crop_type', '').lower()

    recommendations = {
        "wheat": {"Nitrogen": "15", "Phosphorus": "10", "Potassium": "20"},
        "rice": {"Nitrogen": "20", "Phosphorus": "15", "Potassium": "25"},
        "corn": {"Nitrogen": "25", "Phosphorus": "10", "Potassium": "30"},
        "soybean": {"Nitrogen": "18", "Phosphorus": "12", "Potassium": "22"},
        "barley": {"Nitrogen": "14", "Phosphorus": "11", "Potassium": "19"},
        "potato": {"Nitrogen": "20", "Phosphorus": "18", "Potassium": "24"},
        "tomato": {"Nitrogen": "22", "Phosphorus": "14", "Potassium": "28"},
        "sugarcane": {"Nitrogen": "30", "Phosphorus": "20", "Potassium": "35"}
    }

    result = [recommendations.get(crop_type, {"Nitrogen": "15", "Phosphorus": "10", "Potassium": "20"})]
    return jsonify({"fertilizer_recommendations": result})

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
