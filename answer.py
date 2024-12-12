import json

class Answer:
    """
    儲存問卷填寫資料，此類別主要目的為產生填寫問卷的 JSON 格式。
    最終送出的資料格式如下：
    {
        "ANS_ary": [
            {
                "question_id": "20240009",
                "group_id": 1,
                "event_id": "001",
                "teacher_id": "教師編號",
                "course_serial": "課程編號",
                "Subject_id": 1,
                "Data_order": 1,
                "Answer": [
                    {
                        "item_id": 5, # 非常同意
                        "item_next": 2, # 指向下一個問題
                        "item_data": "", # 填空題的答案
                        "item_type": 0 # 0: 單選 1: 填空
                    }
                ]
            },
            ...
        ]
    }
    個人推斷，Answer 裡面的 item_next 應為非必填，但未測試。
    """
    def __init__(
            self,
            teacher_id,
            teacher_name,
            course_serial,
            course_name,
            final_date,
            question_id : str = "20240009",
            group_id : int = 1,
            event_id : str = "001",
    ):
        self.question_id = question_id
        self.group_id = group_id
        self.event_id = event_id
        self.teacher_id = teacher_id
        self.course_serial = course_serial.strip()
        self._teacher_name = teacher_name.strip()
        self._course_name = course_name.strip()
        self._final_date = final_date.strip() # strip 掉空白
        
    @property
    def course_name(self):
        return self._course_name

    @property
    def teacher_name(self):
        return self._teacher_name

    @property
    def final_date(self):
        return self._final_date

    def get_json(self):
        # 產生填寫問卷的 JSON 格式
        survey = {
            "ANS_ary": []
        }

        """
        準備每個題目的答案:
        1. 單選題全填 '非常同意'
        2. 評分填空題，因加總只需 100 分，因此第一題評分題填 100 分，其餘填 0 分
        3. 填空題非必填全填空
        """
        def prepare_answer(index):
            # 30 不會顯示在表單上，因此填空
            # 44, 45 題為填空題，不需填寫
            if index == 30 or index == 44 or index == 45:
                return []

            # 31 ~ 43 題為評分題，第一題填 100 分，其餘填 0 分
            if index < 31 or index > 44:
                return [
                    {
                        "item_id": 5,
                        "item_next": index + 1 if index <= 45 else index, # 最多 45 題，其餘則永遠指向下一題
                        "item_data": "",
                        "item_type": 0
                    }
                ]

            # 除上述兩個 if 以外的題目，填 '非常同意'
            return [
                {
                    "item_id": 6,
                    "item_next": index + 1,
                    "item_data": "100" if index == 31 else "0", # 第一題填 100 分，其餘填 0 分
                    "item_type": 1
                }
            ]

        fill = 65 # 評分題開始，Subject_id 會從 65 開始
        for i in range(1, 46):  # Subject_id 和 Data_order 遞增
            entry = {
                "question_id": "20240009",
                "group_id": 1,
                "event_id": "001",
                "teacher_id": self.teacher_id, # 教師編號
                "course_serial": self.course_serial, # 課程編號
                "Subject_id": fill if i > 30 else i, # 31 ~ 45 題為評分題，Subject_id 遞增
                "Data_order": i,
                "Answer": prepare_answer(i)
            }

            if i > 30: # 31 ~ 45 題為評分題，Subject_id 遞增
                fill += 1

            survey["ANS_ary"].append(entry)

        return json.dumps(survey)

    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'course_serial': self.course_serial,
            'course_name': self.course_name,
            'teacher_name': self.teacher_name,
            'final_date': self.final_date
        }

if __name__ == "__main__":
    answer = Answer("教師編號", "課程編號")
    print(answer.get_json())