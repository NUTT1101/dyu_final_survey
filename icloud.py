import re
from http.cookies import SimpleCookie

import requests

from connection import Connection
from answer import Answer
from api import API


class iCloud:

    @staticmethod
    def login(
            username : str,
            password : str
    ):
        # Login to the iCloud system
        response = requests.post(
            API.login,
            data={"acc": username, "pwd": password}
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception("Failed to connect to the server")

        # Check from alert message if the login is successful
        match = re.search(r'alert\("(.+?)"\)', response.text, re.DOTALL)

        # Check if a match is found, if so, raise an exception
        if match:
            alert_message = match.group(1)  # Get the captured group
            raise Exception(alert_message)
        else: # If no exception is raised, return the connection object
            # Get the PHP session ID from the response headers
            cookie = SimpleCookie(response.headers["Set-Cookie"])
            # Return the connection object, which contains the PHP session ID and the student ID
            return Connection(
                cookie["PHPSESSID"].value,
                username,
            )

    @staticmethod
    def logout(
            conn : Connection
    ):
        response = requests.get(
            API.logout,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        if response.status_code == 302:
            return True
        else:
            raise Exception(f"""
             Failed to logout, code: {response.status_code},
             content: {response.text}
            """)

    @staticmethod
    def list(
            conn : Connection
    ):
        response = requests.get(
            API.list_survey,
            cookies={"PHPSESSID": conn.php_session_id}
        )

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception("Failed to connect to the server")

        json_list = response.json()

        """
        json_list 為 網頁 return 的 json 格式(是一個 json array)，其中一個 element 長這樣:
        {
           "question_no":"20240009",
           "event_no":"001",
           "class_name":"課程名稱",
           "chk_date_QUIZ":1,
           "chk_date_range":"None",
           "question_status":1,
           "final_day":"填單日期  ",
           "final_ip":"填單IP",
           "need_write":1,
           "teacher_name":"教師編號",
           "class_no":"課程編號",
           "fs_day":"填單開始日期時間",
           "fe_day":"填單結束日期時間",
           "json_name":"qmno=20240009&serial=課程編號&teno=教師編號", <-- 這個是填單的網址, return format: json
           "teacher_id":"教師編號",
           "question_array":"None"
        }
        """

        if not json_list or len(json_list) == 0:
            raise Exception("No survey available")

        return [
            Answer(
                teacher_id=i['teacher_id'],
                course_serial=i['class_no']
            ) for i in json_list
        ]

    @staticmethod
    def send(
            conn : Connection,
            answer : Answer
    ):
        res = requests.post(
            API.send_survey,
            cookies={
                "PHPSESSID": conn.php_session_id
            },
            data= {
                "categories" : answer.get_json(),
            }
        )

        if res.status_code < 200 or res.status_code >= 300:
            raise Exception("Failed to submit the survey")

        return res.json()