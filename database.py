from datetime import datetime
from pymongo import MongoClient
import os
from flask import request
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client.dyu_survey
        
    def log_login(self, student_id: str, success: bool):
        """記錄登入嘗試"""
        self.db.login_logs.insert_one({
            'student_id': student_id.upper(),
            'success': success,
            'timestamp': datetime.now(),
            'ip_address': request.remote_addr
        })
    
    def log_survey_completion(self, student_id: str, survey_data: dict):
        """記錄問卷填寫"""
        self.db.survey_logs.insert_one({
            'student_id': student_id.upper(),
            'course_name': survey_data['course_name'],
            'teacher_name': survey_data['teacher_name'],
            'course_serial': survey_data['course_serial'],
            'completed_at': datetime.now(),
            'ip_address': request.remote_addr
        }) 