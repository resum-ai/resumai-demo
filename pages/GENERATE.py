import json
from pages.lib.database_utils import DatabaseManager

import pinecone
import streamlit as st

from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import GENERATE_SELF_INTRODUCTION_PROMPT, GUIDELINE_PROMPT


def create_guidelines(question):
    try:
        if question in ground_guideline:
            return ground_guideline[question]
        else:
            prompt = GUIDELINE_PROMPT.format(question=question)
            guideline_string = get_chat_openai(prompt)
            return json.loads(guideline_string.replace("'", '"'))
    except Exception as e:
        st.error("가이드라인 생성 중 오류가 발생했습니다.")
        print(e)
        return []


def generate_self_introduction(
    favor_info, question, saved_self_introduction, examples_str
):
    try:
        prompt = GENERATE_SELF_INTRODUCTION_PROMPT.format(
            favor_info=favor_info,
            question=question,
            context=saved_self_introduction,
            examples=examples_str,
        )
        generated_self_introduction = get_chat_openai(prompt)
        return generated_self_introduction
    except Exception as e:
        st.error("자기소개서 생성 중 오류가 발생했습니다.")
        print(e)
        return None


def retrieve_similar_answers(saved_self_introduction):
    try:
        pinecone.init(api_key=st.secrets["PINECONE_API_KEY"], environment="gcp-starter")
        index = pinecone.Index("resumai-self-introduction-index")
        query_embedding = get_embedding(saved_self_introduction)
        retrieved_data = index.query(
            vector=query_embedding, top_k=3, include_metadata=True
        )
        return retrieved_data["matches"]
    except Exception as e:
        st.error("유사한 답변 검색 중 오류가 발생했습니다.")
        print(e)
        return []


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

db_manager = DatabaseManager("self_introduction_data.db")
# 테이블 생성
db_manager.create_table()


favor_info = ""
ground_guideline = ""
with open("pages/lib/guideline_data.json", "r", encoding="utf-8") as file:
    ground_guideline = json.load(file)

# 세션 state로 상태 유지
if "guideline_list" not in st.session_state:
    st.session_state["guideline_list"] = []
if "user_answer" not in st.session_state:
    st.session_state["user_answer"] = {}

question = st.radio(
    "답변하고자 하는 질문을 선택하여 가이드라인을 생성해 보세요.",
    ("지원 동기", "직무 관심 계기", "회사 경력", "프로젝트 경험", "성격의 장단점", "어려움 극복 과정", "문제 해결 경험", "기타"),
)

if question == "기타":
    question = st.text_area(
        label="질문 내용을 직접 작성해주세요.", placeholder="질문 내용을 직접 작성해주세요.", height=100
    )

if st.button("가이드라인 생성하기!"):
    with st.spinner("가이드라인을 생성중입니다. 잠시만 기다려주세요."):
        st.session_state["guideline_list"] = create_guidelines(question)


# 각 가이드라인별로 text 입력 필드란 생성
for idx, guideline in enumerate(st.session_state["guideline_list"]):
    st.session_state["user_answer"][guideline] = st.text_area(
        label=guideline,
        placeholder=guideline,
        height=200,
        key=f"guideline_{idx}",
    )

# 기업 우대사항 작성란
if st.session_state["guideline_list"]:
    favor_info = st.text_area(
        label="기업 공고의 우대사항을 작성해 주세요.", placeholder="우대사항", height=200
    )

if st.session_state["user_answer"]:
    if st.button("자기소개서 생성하기!"):
        with st.spinner("답변을 생성중입니다. 잠시만 기다려주세요."):
            # 답변 취합
            saved_self_introduction = "\n\n".join(
                [
                    st.session_state["user_answer"][guideline]
                    for guideline in st.session_state["guideline_list"]
                ]
            )
            examples = retrieve_similar_answers(saved_self_introduction)
            examples_str = "\n\n".join(
                [
                    f"예시{i}) \nQuestion: {ex['metadata']['question']} \nAnswer: {ex['metadata']['answer']}"
                    for i, ex in enumerate(examples, start=1)
                ]
            )

            prompt = GENERATE_SELF_INTRODUCTION_PROMPT.format(
                favor_info=favor_info,
                question=question,
                context=saved_self_introduction,
                examples=examples_str,
            )
            print(prompt)

            generated_self_introduction = generate_self_introduction(
                favor_info, question, saved_self_introduction, examples_str
            )

            if generated_self_introduction:
                st.success("답변이 생성되었습니다!")
                st.write(generated_self_introduction)
            else:
                st.error("답변 생성에 실패했습니다..")

            # db 저장을 위해 list에서 json으로 변경
            generated_guideline_json = json.dumps(st.session_state["guideline_list"])

            db_manager.save_to_db(
                question,
                generated_guideline_json,
                saved_self_introduction,
                favor_info,
                examples_str,
                generated_self_introduction,
            )

            # 데이터베이스 연결 종료
            db_manager.close()
