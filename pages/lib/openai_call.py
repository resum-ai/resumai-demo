import os

import streamlit
from openai import OpenAI


client = OpenAI(api_key=streamlit.secrets["OPENAI_API_KEY"])


def get_chat_openai(prompt, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    output = response.choices[0].message.content
    return output


def get_embedding(text, model="text-embedding-ada-002"):
    # text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model).data
    response = response[0].embedding
    return response
