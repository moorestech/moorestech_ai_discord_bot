import os

import anthropic
from openai import OpenAI

SYSTEM_PROMPT = "This is part of the moorestech code. Please refer to this and follow the instructions."

openai_client = OpenAI()
claude_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


class ModelType:
    GPT4 = 1,
    Claude3 = 2,


def query_ai(prompt, model_type):
    response = ""
    if model_type == ModelType.GPT4:
        messages = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}]

        completion = openai_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
            temperature=0.2,
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
