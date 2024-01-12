import json

import pinecone
import streamlit as st

from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import GENERATE_SELF_INTRODUCTION_PROMPT, GUIDELINE_PROMPT

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

ground_guideline = ""
with open("pages/lib/guideline_data.json", "r", encoding="utf-8") as file:
    ground_guideline = json.load(file)

favor_info = ""

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
        try:
            st.session_state["guideline_list"] = ground_guideline[question]
        except KeyError:
            prompt = GUIDELINE_PROMPT.format(question=question)

            # 프롬프트로 생성한 가이드라인
            guideline_string = get_chat_openai(prompt)

            # 생성된 string 형태의 가이드라인을 list로 변환
            st.session_state["guideline_list"] = json.loads(
                guideline_string.replace("'", '"')
            )


# 각 가이드라인별로 text 입력 필드 생성
for idx, guideline in enumerate(st.session_state["guideline_list"]):
    st.session_state["user_answer"][guideline] = st.text_area(
        label=guideline,
        placeholder=guideline,
        height=200,
        key=f"guideline_{idx}",  # 각 text_area에 고유한 key 제공
    )

# 기업 우대사항
if st.session_state["guideline_list"]:
    favor_info = st.text_area(
        label="기업 공고의 우대사항을 작성해 주세요.", placeholder="우대사항", height=200
    )

if st.session_state["user_answer"]:
    if st.button("자기소개서 생성하기!"):
        with st.spinner("답변을 생성중입니다. 잠시만 기다려주세요."):
            # 답변 취합
            saved_self_introduction = ""

            for guideline in st.session_state["guideline_list"]:
                saved_self_introduction += (
                    f'{st.session_state["user_answer"][guideline]} \n\n'
                )
            print(saved_self_introduction)

            # vectorDB에서 유사한 데이터 검색
            pinecone.init(
                api_key=st.secrets["PINECONE_API_KEY"], environment="gcp-starter"
            )
            index = pinecone.Index("resumai-self-introduction-index")

            query_embedding = get_embedding(
                saved_self_introduction
            )  # 유저가 질문에 답변한 것을 임베딩
            retrieved_data = index.query(
                vector=query_embedding, top_k=3, include_metadata=True
            )  # 유사한 top 3개의 답변

            data = retrieved_data["matches"]

            data_1_question = data[0]["metadata"]["question"]
            data_1_answer = data[0]["metadata"]["answer"]

            data_2_question = data[1]["metadata"]["question"]
            data_2_answer = data[1]["metadata"]["answer"]

            data_3_question = data[2]["metadata"]["question"]
            data_3_answer = data[2]["metadata"]["answer"]

            # 프롬프트 예시
            examples = (
                f"예시1) \n Question: {data_1_question}, \n Answer: {data_1_answer}, \n\n "
                f"예시2) \n Question: {data_2_question}, \n Answer: {data_2_answer}, \n\n "
                f"예시3) \nQuestion: {data_3_question}, \n Answer: {data_3_answer}"
            )

            prompt = GENERATE_SELF_INTRODUCTION_PROMPT.format(
                favor_info=favor_info,
                question=question,
                context=saved_self_introduction,
                examples=examples,
            )

            answer = get_chat_openai(prompt)

            if answer:
                st.success("답변이 생성되었습니다!")
                st.write(answer)
            else:
                st.error("답변 생성에 실패했습니다..")

            print(answer)
