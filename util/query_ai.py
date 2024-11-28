import os
import anthropic
from openai import OpenAI

SYSTEM_PROMPT = ("これは moorestech コードの一部です。これを参照して指示に従ってください。また、1500字以内で簡潔に回答してください。"
                 "なお、回答をするときの口調として、元気でハツラツな女の子の印象を持つような口調で回答するように心がけてください。")

openai_client = OpenAI()
claude_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class ModelType:
    GPT4 = 1
    Claude3 = 2


def query_ai(prompt, model_type):
    response = ""
    if model_type == ModelType.GPT4:
        messages = [{'role': 'user', 'content': SYSTEM_PROMPT + prompt}]

        completion = openai_client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=messages,
        )
        response = completion.choices[0].message.content
    elif model_type == ModelType.Claude3:
        # Claude-3

        message = claude_client.messages.create(
            model="claude-3-opus-20240229",
            system=SYSTEM_PROMPT,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        response = message.content[0].text

    return response

async def query_ai_stream_gpt4(prompt):
    messages = [{'role': 'user', 'content': SYSTEM_PROMPT + prompt}]
    print(prompt)
    stream = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="")
            yield content

