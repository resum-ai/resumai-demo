import sqlite3
import json


class DatabaseManager:
    # 데이터베이스 연결
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # 저장하려는 데이터: 답변하고자 하는 질문, 생성된 가이드라인, 작성한 데이터, 우대공고, 생성된 자기소개서
    def create_table(self):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS self_introduction_data (
                question TEXT,
                generated_guideline TEXT,
                user_answer TEXT,
                favor_info TEXT,
                examples TEXT,
                generated_self_introduction TEXT
            )
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    # 데이터베이스 저장
    def save_to_db(
        self,
        question,
        generated_guideline,
        user_answer,
        favor_info,
        examples,
        generated_self_introduction,
    ):
        insert_sql = """
            INSERT INTO self_introduction_data (
                question, generated_guideline, user_answer, favor_info, examples, generated_self_introduction
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            insert_sql,
            (
                question,
                json.dumps(generated_guideline),
                user_answer,
                favor_info,
                examples,
                generated_self_introduction,
            ),
        )
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM self_introduction_data")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
