# SUMMARY_PROMPT = f"""{{text}}
# ---
# Must respond in {{language}}.
# Tl;dr
# """
#
# TRANSLATE_PROMPT = f"""sentence={{text}}
# ---
# sentence를 번역해주세요.
# Must respond in {{language}}.
# """


GENERATE_SELF_INTRODUCTION_PROMPT = f"""
자기소개서를 작성하는데, 다음 질문에 답하려고 합니다.
Question: {{question}} \n

질문에 대한 저의 대답은 다움과 같습니다.
Context: {{context}} \n

아래는 몇 가지 예시입니다.
examples: {{examples}} 

예시들과 저의 답변을 참고하여 질문에 대한 대답을 해 주세요.
"""
