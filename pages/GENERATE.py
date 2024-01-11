import json

import pinecone
import streamlit as st

from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import GENERATE_SELF_INTRODUCTION_PROMPT, GUIDELINE_PROMPT

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

ground_guideline = {
    "지원 동기": [
        "지원하는 회사에 대한 이해와 그 회사에서 일하고 싶은 이유를 서술해 주세요.",
        "지원하는 직무에 대한 이해와 그 직무를 수행하고 싶은 이유를 서술해 주세요.",
        "지원하는 회사와 으로 지원 동기를 서술해 주세요.",
        "지원하는 직무를 수행하기 위해 필요한 당신의 능력과 경험을 서술해 주세요.",
    ],
    "직무 관심 계기": [
        "어떤 경험 또는 사건이 직무에 관심을 갖게 했는지 구체적으로 작성해 주세요.",
        "이 직무에 대해 더 알아가고 싶었던 이유를 서술해 주세요.",
        "관련 경험(학습, 프로젝트, 인턴, 아르바이트 등)을 어떻게 진행했는지 서술해 주세요.",
        "직무에 대한 이해와 관심이 어떻게 성장했는지 서술해 주세요.",
        "이 직무를 통해 이루고 싶은 장기적 목표가 있다면 함께 서술해 주세요.",
    ],
    "회사 경력": [
        "이전 직장에서의 주요 업무와 책임을 상세하게 작성해 주세요.",
        "경력 기간 동안 이룬 성과와 결과를 구체적인 예시와 함께 서술해 주세요.",
        "직장에서 겪었던 어려움과 이를 극복한 과정을 서술해 주세요.",
        "해당 경력이 지원하는 직무에 어떻게 도움이 될 수 있는지 연결하여 서술해 주세요.",
        "직장에서의 학습 경험과 개인적 성장을 서술해 주세요.",
    ],
    "프로젝트 경험": [
        "프로젝트의 목적과 당신의 역할을 명확하게 작성해 주세요.",
        "프로젝트를 수행하며 사용한 기술, 도구, 방법론에 대해 서술해 주세요.",
        "프로젝트 과정에서 발생한 주요 도전과 이를 어떻게 극복했는지 서술해 주세요.",
        "프로젝트 결과와 이를 통해 얻은 교훈 또는 성과를 구체적으로 작성해 주세요.",
        "이 프로젝트 경험이 어떻게 당신의 전문성을 강화했는지 서술해 주세요.",
    ],
    "성격의 장단점": [
        "자신의 성격에서 가장 강점이라고 생각하는 부분을 서술해 주세요.",
        "이러한 강점이 업무나 일상생활에서 어떻게 긍정적인 영향을 끼쳤는지 예시와 함께 작성해 주세요.",
        "성격의 단점이나 개선이 필요한 부분을 솔직하게 서술해 주세요.",
        "이 단점을 극복하기 위해 어떤 노력을 하고 있는지 구체적으로 작성해 주세요.",
        "성격의 장단점이 해당 직무와 어떻게 연관되는지 분석하여 서술해 주세요.",
    ],
    "어려움 극복 과정": [
        "어려움을 경험한 구체적인 상황을 설명해 주세요.",
        "이 어려움이 당신에게 어떤 영향을 끼쳤는지 서술해 주세요.",
        "어려움을 극복하기 위해 구체적으로 어떤 노력을 했는지 작성해 주세요.",
        "극복 과정에서 얻은 교훈이나 개인적인 성장에 대해 서술해 주세요.",
        "이러한 경험이 앞으로 어떻게 당신을 도울 것인지 연결하여 서술해 주세요.",
    ],
    "문제 해결 경험": [
        "문제가 발생한 상황과 그 문제의 본질을 명확하게 서술해 주세요.",
        "문제 해결을 위해 구상한 다양한 해결책과 접근 방법을 작성해 주세요.",
        "최종적으로 선택한 해결책과 그 이유를 서술해 주세요.",
        "문제 해결 과정에서 어떤 도전과 어려움이 있었는지 서술해 주세요.",
        "문제 해결 결과와 이를 통해 배운 교훈을 서술해 주세요.",
    ],
}
favor_info = ""

# 스트림릿의 세션 상태를 사용하여 상태 유지
if "guideline_list" not in st.session_state:
    st.session_state["guideline_list"] = []
if "user_answer" not in st.session_state:
    st.session_state["user_answer"] = {}

question = st.radio(
    "답변하고자 하는 질문을 선택해주세요.",
    ("지원 동기", "직무 관심 계기", "회사 경력", "프로젝트 경험", "성격의 장단점", "어려움 극복 과정", "문제 해결 경험", "기타"),
)

if question == "기타":
    question = st.text_input("질문 내용을 직접 작성해주세요.")

if st.button("가이드라인 생성하기!"):
    with st.spinner("가이드라인을 생성중입니다. 잠시만 기다려주세요."):
        try:
            # 기존에 ground_guideline을 사용하고 있다면, 이를 st.session_state로 대체
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
        placeholder=f"{guideline}에 대한 자신의 경험을 간단하게 소개해주세요.",
        height=200,
        key=f"guideline_{idx}",  # 각 text_area에 고유한 key 제공
    )

# 기업 우대사항
favor_info = st.text_area(label="기업 공고의 우대사항을 작성해 주세요.", placeholder="우대사항", height=200)


if st.button("자기소개서 생성하기!"):
    with st.spinner("답변을 생성중입니다. 잠시만 기다려주세요."):
        # 답변 취합
        saved_self_introduction = ""

        for guideline in st.session_state["guideline_list"]:
            saved_self_introduction += (
                f'# {guideline} \n {st.session_state["user_answer"][guideline]} \n\n'
            )
        print(saved_self_introduction)

        # vectorDB에서 유사한 데이터 검색
        pinecone.init(api_key=st.secrets["PINECONE_API_KEY"], environment="gcp-starter")
        index = pinecone.Index("resumai-self-introduction-index")

        query_embedding = get_embedding(saved_self_introduction)  # 유저가 질문에 답변한 것을 임베딩
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
