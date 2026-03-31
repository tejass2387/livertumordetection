import os
from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from src.predict import get_full_prediction
# Re-enabled the AI report import
from src.ai_report import generate_report 

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- YOUR EXISTING DASHBOARD ROUTE ---
# This is the main analysis page
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files: return redirect(request.url)
        file = request.files['file']
        if file.filename == '': return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result_filename, detection_status, tumor_type = get_full_prediction(filepath)
            
            return render_template('index.html', 
                                   result_filename=result_filename, 
                                   detection_status=detection_status,
                                   tumor_type=tumor_type)
    
    # This just shows the main page (if not a POST request)
    return render_template('index.html')

# --- NEW ROUTES FOR AUTHENTICATION ---

@app.route('/login')
def login_page():
    """Serves the login page."""
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    """Serves the signup page."""
    return render_template('signup.html')

@app.route('/forgot-password')
def forgot_password_page():
    """Serves the forgot password page."""
    return render_template('forgot_password.html')

# --- RE-ENABLED AI REPORT ROUTE ---
@app.route('/generate-report', methods=['POST'])
def handle_ai_report():
    data = request.get_json()
    status = data.get('status')
    tumor_type = data.get('tumor_type')
    
    report = generate_report(status, tumor_type)
    
    return jsonify({'report': report})

# --- YOUR SERVER STARTUP IS UNCHANGED ---
if __name__ == '__main__':
    app.run(debug=True)