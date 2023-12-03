import json

from prompts import SUMMARY_PROMPT
from flask import Flask, request
from openai_call import get_chat_openai

app = Flask(__name__)


# @app.route("/llm_summary/predict", methods=["GET", "POST"])
def llm_summary():
    # params = json.loads(request.get_data(), encoding="utf-8")

    # text = params["text"]
    # language = params["language"]

    prompt = SUMMARY_PROMPT.format(text=""" Any request to read a sector will cause that sector and much or
all the rest of the current track to be read, depending upon how
much space is available in the controller’s cache memory
•""", language='한국어')
    result_summary = get_chat_openai(prompt)
    print(result_summary)

    return {"summary": result_summary}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="1000")
    llm_summary()
