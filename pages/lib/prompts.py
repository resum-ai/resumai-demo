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
examples: {{qa}} \n
Question: {{question}} \n

exmaples과 비슷한 형식으로 Question에 대한 대답을 다음을 참고하여 대답해 주세요. \n

Context: {{context}}
"""
