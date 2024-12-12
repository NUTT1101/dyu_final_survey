class API:
    """
    儲存 API 的網址
    """

    login = "https://icloud.dyu.edu.tw/login.php?data=" # 登入 url, method: POST, data: {"acc": "學號", "pwd": "密碼"}, format: x-www-form-urlencoded
    logout = "https://icloud.dyu.edu.tw/logout.php" # 登出 url, method: GET, cookies: {"PHPSESSID": "PHP session id"}
    # 列出所有問卷 url, method: GET, cookies: {"PHPSESSID": "PHP session id"}
    list_survey = "https://icloud.dyu.edu.tw/forms/api/API_Graduates_chk.php?gLanguage=0&year=113&semester=1&gSys_s=que&gFunc_s=NXZ3dW81Q1laQ0lnekYrcWE0U3Iwdz09&gGroups_i=0&_=1733895694702"
    # 填寫問卷 url, method: POST, data: {詳見 answer.py}, format: x-www-form-urlencoded
    send_survey = "https://icloud.dyu.edu.tw/forms/api/API_Course_save.php?gSys_s=que&gFunc_s=NXZ3dW81Q1laQ0lnekYrcWE0U3Iwdz09&gGroups_i=0&year=113&semester=1&quiz_type=12"