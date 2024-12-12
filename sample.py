from icloud import iCloud

if __name__ == "__main__":
    # 登入至 iCloud 系統，請將 "帳號" 和 "密碼" 替換成自己的帳號密碼
    conn = iCloud.login("帳號", "密碼")
    # 取得所有問卷
    survey_list = iCloud.list(conn)
    # 逐一填寫問卷
    for survey in survey_list:
        r = iCloud.send(conn, survey)
        if int(r["save_status"]) == 1:
            print(f"{survey.course_serial} Survey submitted successfully")
        else:
            print(f"{survey.course_serial} Survey submission failed")
    # 登出
    iCloud.logout(conn)