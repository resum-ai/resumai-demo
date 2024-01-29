import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Streamlit secrets에서 서비스 계정 정보 가져오기
service_account_info = st.secrets["connections"]["gsheets"]
credentials = Credentials.from_service_account_info(service_account_info)

# 사용할 Google API의 스코프 정의
scoped_credentials = credentials.with_scopes(
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
)

# gspread 클라이언트 초기화
gc = gspread.authorize(scoped_credentials)

# 구글 시트 열기 (시트 이름 또는 URL 사용)
spreadsheet_name_or_url = "resumai-demo-db"
sh = gc.open(spreadsheet_name_or_url)
worksheet = sh.sheet1  # 첫 번째 워크시트 선택


def add_data_to_sheet(
    question,
    generated_guideline,
    user_answer,
    favor_info,
    examples,
    generated_self_introduction,
):
    try:
        # 시트에 새로운 행 추가
        worksheet.append_row(
            [
                question,
                generated_guideline,
                user_answer,
                favor_info,
                examples,
                generated_self_introduction,
            ]
        )
        return {"status": "success", "code": 200}
    except gspread.exceptions.APIError as e:
        # Google Sheets API 에러 처리
        return {"status": "error", "code": e.response.status_code, "message": str(e)}
    except Exception as e:
        # 기타 예외 처리
        return {"status": "error", "code": 500, "message": str(e)}


def add_comment_to_sheet(user_comment):
    try:
        # 마지막으로 데이터를 추가한 행을 찾기
        last_row = worksheet.row_count

        # 마지막 열(예: Comments 열)의 번호를 찾기
        comment_column_number = worksheet.col_count

        # 마지막 행의 'Comments' 열에 데이터 업데이트
        worksheet.update_cell(last_row, comment_column_number, user_comment)
        return {"status": "success", "code": 200}
    except gspread.exceptions.APIError as e:
        # Google Sheets API 에러 처리
        return {"status": "error", "code": e.response.status_code, "message": str(e)}
    except Exception as e:
        # 기타 예외 처리
        return {"status": "error", "code": 500, "message": str(e)}
