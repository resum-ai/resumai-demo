import pickle
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import SEARCH_PROMPT

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


question = st.radio(
    "대답하고자 하는 질문을 선택해주세요.",
    ("지원 동기", "직무 관심 계기", "회사 경력", "프로젝트 경험", "성격의 장단점", "어려움 극복 과정"),
)
user_answer = st.text_area(question)
if st.button("DB 내의 비슷한 질문에 대한 답변 찾아보기"):
    query_embedding = get_embedding(user_answer)
    with open("self_introductions.pickle", "rb") as f:
        total_data = pickle.load(f)

    question_list = total_data["question_list"]
    answer_list = total_data["answer_list"]
    question_embedding = total_data["question_embedding"]

    query_embedding = np.array(query_embedding)
    context_embedding = np.array(question_embedding)

    similarity_scores = cosine_similarity([query_embedding], context_embedding)
    print(similarity_scores)
    max_index = np.argmax(
        similarity_scores
    )  # TODO: argmax 말고 top3의 유사한 유사한 context를 얻어야 함 (few-shot으로 주기 위함)

    retrieved_question = question_list[max_index]
    retrieved_answer = answer_list[max_index]

    # prompt = SEARCH_PROMPT.format(context=context, question=sentence)
    # answer = get_chat_openai(prompt)

    st.markdown(f"### {retrieved_question}")
    st.write(retrieved_answer)
    # st.markdown("### 답변")
    # st.write(answer)
