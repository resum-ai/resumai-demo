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

sentence = st.text_input("회사에 지원하게 된 동기에 대해서 설명해주세요.")
if st.button("답변 생성"):
    query_embedding = get_embedding(sentence)
    with open("self_introductions.pickle", "rb") as f:
        total_data = pickle.load(f)

    answer_list = total_data["answer_list"]
    question_embedding = total_data["question_embedding"]

    query_embedding = np.array(query_embedding)
    context_embedding = np.array(question_embedding)

    similarity_scores = cosine_similarity([query_embedding], context_embedding)
    max_index = np.argmax(similarity_scores)

    context = answer_list[max_index]

    # prompt = SEARCH_PROMPT.format(context=context, question=sentence)
    # answer = get_chat_openai(prompt)

    st.markdown("### 마크다운")
    st.write(context)
    # st.markdown("### 답변")
    # st.write(answer)
