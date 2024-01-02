import json

from prompts import SUMMARY_PROMPT, GENERATE_SELF_INTRODUCTION_PROMPT
from flask import Flask, request
from openai_call import get_chat_openai

app = Flask(__name__)


# @app.route("/llm_summary/predict", methods=["GET", "POST"])
def llm_summary():
    # params = json.loads(request.get_data(), encoding="utf-8")

    # text = params["text"]
    # language = params["language"]

    prompt = GENERATE_SELF_INTRODUCTION_PROMPT.format(qa="", question="한국어", context="")
    result_summary = get_chat_openai(prompt)
    print(result_summary)

    return {"summary": result_summary}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="1000")
    llm_summary()
