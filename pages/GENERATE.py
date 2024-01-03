import pinecone
import streamlit as st

from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import GENERATE_SELF_INTRODUCTION_PROMPT

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

question = st.radio(
    "답변하고자 하는 질문을 선택해주세요.",
    ("지원 동기", "직무 관심 계기", "회사 경력", "프로젝트 경험", "성격의 장단점", "어려움 극복 과정", "문제 해결 경험"),
)

user_answer = st.text_area(
    label=question, placeholder=f"{question}에 대한 자신의 경험을 간단하게 소개해주세요.", height=300
)

if st.button("생성하기!"):
    with st.spinner("답변을 생성중입니다. 잠시만 기다려주세요."):

        pinecone.init(api_key=st.secrets["PINECONE_API_KEY"], environment="gcp-starter")
        index = pinecone.Index("resumai-self-introduction-index")

        query_embedding = get_embedding(user_answer) # 유저가 질문에 답변한 것을 임베딩

        retrieved_data = index.query(vector=query_embedding, top_k=3, include_metadata=True) # 유사한 top 3개의 답변

        data = retrieved_data["matches"]

        data_1_question = data[0]["metadata"]["question"]
        data_1_answer = data[0]["metadata"]["answer"]

        data_2_question = data[1]["metadata"]["question"]
        data_2_answer = data[1]["metadata"]["answer"]

        data_3_question = data[2]["metadata"]["question"]
        data_3_answer = data[2]["metadata"]["answer"]

        examples = (
            f"Question: {data_1_question}, \n Answer: {data_1_answer}, \n\n "
            f"Question: {data_2_question}, \n Answer: {data_2_answer}, \n\n "
            f"Question: {data_3_question}, \n Answer: {data_3_answer}"
        )

        prompt = GENERATE_SELF_INTRODUCTION_PROMPT.format(
            examples=examples, question=question, context=user_answer
        )

        answer = get_chat_openai(prompt)

        if answer:
            st.success("답변이 생성되었습니다!")
            st.write(answer)
        else:
            st.error("답변 생성에 실패했습니다..")

    print(answer)

