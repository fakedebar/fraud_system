from flask import Flask, request, render_template, send_file
import os
from process_file import process_file

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
app = Flask(__name__, template_folder='../templates')


# تأكد من وجود مجلدات للرفع والنتائج
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')
    if request.method == ['GET', 'POST']:
        username = request.form.get('username')
        password = request.form.get('password')

@app.route('/upload')
def upload():
    return render_template('upload.html')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None  # Initialize the message as None
    if request.method == 'POST':  # Handle form submission
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Add your authentication logic here
        if username == "admin" and password == "password123":
            message = "Login successful!"
        else:
            message = "Invalid username or password."

    # Pass the message to the template
    return render_template('login.html', message=message)




# معالجة الملفات المرفوعة
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    # حفظ الملف المرفوع
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # تحليل الملف (أضف كود التحليل هنا)
    result_filepath = process_file(filepath)

    # إعادة الملف الناتج إلى المستخدم
    return send_file(result_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3300)
