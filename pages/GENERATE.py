import pickle
import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pages.lib.openai_call import get_embedding, get_chat_openai
from pages.lib.prompts import SEARCH_PROMPT
from pages.lib.store_vector import store_vector

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

data = [
    {
        "Question": "[지원동기] 우리 회사 체험형 인턴 프로그램에 지원한 목적을 서술해 주십시오.",
        "Answer": """
            "서부발전의 스마트플랜트 구축에 기여하는 인재"
            저는 저의 다양한 소프트웨어 지식과 경험을 통해 한국서부발전의 효율적인 발전 시스템 구축에 기여하고 싶습니다. 한국서부발전의 사업 목록 중, 디지털 기술기반 WP-스마트플랜트 구축 사업을 보게 되었습니다. 저는 다양한 데이터를 다루어 보았던 경험과, 인공지능, IoT기술을 활용하여 문제를 해결하였던 경험, 그리고 모바일 플랫폼 구축 경험이 있습니다. 이러한 경험들을 응용하여, 저는 발전 현장에서 응용할 수 있는 데이터 분석법 도출, 모바일 플랫폼 구축 및 IoT 기반 안전사고 예방 시스템 구축에 도움을 드릴 수 있도록 노력하겠습니다.
            그리고 발전 현장에서의 정보통신직무의 업무 프로세스에 대해 배우고 싶습니다. 이번 인턴 업무로 저는 정보통신 직무가 어떤 방식으로 사업을 진행하는지 학습할 것입니다. 이 경험을 체계적으로 정리하여 이후 제가 한국서부발전에 입사할 시 빠른 업무 적응과 원활한 사업 진행을 할 수 있도록 하겠습니다.
        """
    },
    {
        "Question": "[자기개발노력] 지원 분야에 대해 관심을 갖게 된 계기와 해당분야 직무역량 개발을 위해 꾸준히 노력한 경험을 서술해 주십시오.",
        "Answer": """
            "전공지식과 문제 해결 경험 함양"
            제 전공이 컴퓨터과학부여서, 자연스럽게 디지털 뉴딜 및 발전 현장의 디지털 플랫폼화에 관심을 가지게 되었습니다. 위의 사업에 맞는 역량을 가질 수 있도록, 다양한 소프트웨어 지식 및 경험을 함양할 수 있도록 노력하였습니다. 먼저, 컴퓨터 알고리즘, 운영체제, 자료구조와 같은 전공과목들을 우수한 성적으로 수료하였습니다.
            또한, 실제 문제 해결 경험을 쌓기 위해, 00시의 문제를 빅데이터를 응용하여 해결책을 제시하는 공모전에 참여하였습니다. 저는 00시의 불법 주정차로 인한 어린이 보호구역에서의 사고를 줄이고자 하였습니다. 00시의 교통 데이터(불법 주정차 단속 데이터, 어린이 보호구역 데이터 등)를 python으로 분석하여 위험 지대를 찾아내었습니다. 이를 바탕으로 불법 주정차 단속 경로를 추천하였고, 현실적인 해결책임을 인정받아 은상을 수상하였습니다. 이런 노력과 경험을 활용하여, 적극적으로 문제를 찾아내고 이를 SW 기술을 활용하여 해결하겠습니다.
        """
    },
    {
        "Question": "[조직적응능력] 조직이나 단체에 소속되어 해당조직의 목표달성을 위해 본인이 수행했던 역할 및 성과를 서술하고, 인턴기간 중 본인이 우리 회사에 기여할 수 있는 바를 작성해 주십시오.",
        "Answer": """
            "팀과 함께 실제 서비스를 개발하였습니다"
            캡스톤 프로젝트를 진행하며 4인으로 모바일 어플을 개발했던 경험이 있습니다. 저희 팀은 코로나 시대에 더욱 편리하게 비대면 취미를 즐길 수 있도록, 독서모임 관리 어플을 개발하기로 하였습니다. 기존의 서비스와 차별화를 두기 위해, 누구나 쉽게 모임을 생성하는 기능을 탑재했고, OCR 기술로 쉽게 독후감을 공유할 수 있도록 하였습니다. 모임 관리에 필수적인 일정관리 기능과, AI를 이용하여 사용자에게 키워드를 받으면 알맞은 도서를 추천하는 기능도 도입하였습니다.
            저는 이를 위해 React Native로 프론트엔드를 구축하였고, Firebase DBMS로 DB를 구축하여 프론트엔드와 연동하였습니다. 또한 팀원들과 매주 2번의 회의와 메신저를 이용한 꾸준한 소통을 통해 완성도 높은 서비스를 완성할 수 있었습니다. 이런 경험을 살려, 저는 한국서부발전의 디지털 플랫폼의 모바일 연동이나 인공지능을 이용한 데이터 분석 사업에 기여하도록 하겠습니다.
        """
    },
    {
        "Question": "[변화혁신] 기존의 비효율적인 관행에 대해 문제의식을 갖고, 이를 주도적으로 해결했던 경험에 대해 작성해 주십시오.",
        "Answer": """
            "공학적 설계로 현실의 문제를 해결하다"
            현재 코로나 바이러스로 인해 건물을 출입할 때에는 체온 측정과 손소독제 공급 과정이 필수가 되었습니다. 저는 사람이 많이 몰리는 건물의 경우, 이 과정이 비효율적이고 사람과의 접촉이 발생하기에 바이러스의 감염 위험 또한 존재한다고 판단하였습니다.
            저는 다양한 센서와 arduino를 이용해 이 두 과정을 자동화한 솔루션인 코로나 원 패스를 개발하여 문제를 해결하고자 하였습니다. 사용자가 기기에 손을 내밀면 비접촉 체온 센서가 체온을 측정하며, 이후 체온 측정 결과를 디스플레이에 표시하여 사용자에게 피드백 해줍니다. 이후 같이 설치된 워터펌프로 사용자의 손에 바로 손소독제를 공급해 주도록 하였습니다. 과제물 제출 결과, 인력 소모를 없앤 현실적인 해결책이라는 점에서, 높은 평가점수를 받을 수 있었습니다. 저는 위의 경험을 응용해 한국서부발전에서도 문제를 주도적으로 찾고 이를 공학적 프로세스를 활용하여 해결해 나가겠습니다.
        """
    },

]


with st.spinner('답변 생성을 위한 사전 작업을 준비중입니다. 잠시만 기다려주세요.'):
    status_code = store_vector(data)
    if status_code == 200:
        st.success('사전 작업이 완료되었습니다!')
    else:
        st.error(f'사전 작업이 다음 code로 실패하였습니다.: {status_code}')

question = st.radio("대답하고자 하는 질문을 선택해주세요.", ("지원 동기", "직무 관심 계시", "회사 경력", "프로젝트 경험", "성격의 장단점", "어려움 극복 과정"))
sentence = st.text_area(question)
if st.button("DB 내의 비슷한 질문에 대한 답변 찾아보기"):
    query_embedding = get_embedding(sentence)
    with open("self_introductions.pickle", "rb") as f:
        total_data = pickle.load(f)

    question_list = total_data["question_list"]
    answer_list = total_data["answer_list"]
    question_embedding = total_data["question_embedding"]

    query_embedding = np.array(query_embedding)
    context_embedding = np.array(question_embedding)

    similarity_scores = cosine_similarity([query_embedding], context_embedding)
    max_index = np.argmax(similarity_scores) # TODO: argmax 말고 top3의 유사한 유사한 context를 얻어야 함 (few-shot으로 주기 위함)

    retrieved_question = question_list[max_index]
    retrieved_answer = answer_list[max_index]

    # prompt = SEARCH_PROMPT.format(context=context, question=sentence)
    # answer = get_chat_openai(prompt)

    st.markdown(f"### {retrieved_question}")
    st.write(retrieved_answer)
    # st.markdown("### 답변")
    # st.write(answer)