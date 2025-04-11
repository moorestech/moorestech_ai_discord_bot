import os
import anthropic
from openai import OpenAI

SYSTEM_PROMPT = "これは moorestech コードの一部です。これを参照して指示に従ってください。また、1500字以内で簡潔に回答してください。"

openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)



def query_ai(prompt):
    messages = [{'role': 'user' , 'content': SYSTEM_PROMPT + prompt}]

    completion = openai_client.chat.completions.create(
        model="anthropic/claude-3.7-sonnet" ,
        messages=messages ,
    )
    response = completion.choices[0].message.contentd

    return response

async def query_ai_stream(prompt):
    messages = [{'role': 'user', 'content': SYSTEM_PROMPT + prompt}]
    print(prompt)
    stream = openai_client.chat.completions.create(
        model="anthropic/claude-3.7-sonnet" ,
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="")
            yield content

