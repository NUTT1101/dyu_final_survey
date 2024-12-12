from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from functools import wraps
from connection import Connection
from answer import Answer
from database import Database
import os
from dotenv import load_dotenv
from icloud import iCloud

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.getenv('SECRET_KEY')
db = Database()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'php_session_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        agree_terms = request.form.get('agreeTerms')
        
        if not agree_terms:
            flash('請先閱讀並同意使用條款', 'error')
            return render_template('login.html')
        
        try:
            # 嘗試登入
            conn = iCloud.login(username, password)
            # 儲存 session
            session['php_session_id'] = conn.php_session_id
            session['student_id'] = username  # 儲存學號
            # 記錄成功登入
            db.log_login(username, True)
            return redirect(url_for('dashboard'))
        except Exception as e:
            # 記錄失敗登入
            db.log_login(username, False)
            flash(str(e), 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        conn = Connection(session['php_session_id'])
        surveys = iCloud.list(conn)
        surveys_data = [survey.to_dict() for survey in surveys]
        return render_template('dashboard.html', surveys=surveys_data)
    except Exception as e:
        flash(str(e), 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'php_session_id' in session:
        try:
            conn = Connection(session['php_session_id'])
            iCloud.logout(conn)
        except:
            pass
        session.clear()
    return redirect(url_for('login'))

@app.route('/fill_survey', methods=['POST'])
@login_required
def fill_survey():
    try:
        data = request.json
        conn = Connection(session['php_session_id'])
        survey = Answer(
            teacher_id=data['teacher_id'],
            course_serial=data['course_serial'],
            teacher_name=data['teacher_name'],
            course_name=data['course_name'],
            final_date=data['final_date']
        )
        result = iCloud.send(conn, survey)
        success = int(result["save_status"]) == 1
        
        if success:
            # 記錄問卷填寫
            db.log_survey_completion(session['student_id'], data)
        
        return jsonify({
            'success': success
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')