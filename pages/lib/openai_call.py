import os
from openai import OpenAI


client = OpenAI(api_key='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')


def get_chat_openai(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10,
        temperature=0,
    )
    output = response.choices[0].message.content
    return output


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   response = client.embeddings.create(input=[text], model=model).data
   response = response[0].embedding
   return response
