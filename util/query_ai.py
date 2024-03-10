from enum import Enum
from openai import OpenAI

openai_client = OpenAI()


class ModelType:
    GPT4 = 1,
    Claude3 = 2,


def query_ai(prompt, model_type):
    response = ""
    if model_type == ModelType.GPT4:
        messages = [
            {'role': 'system',
             'content': 'This is part of the moorestech code. Please refer to this and follow the instructions.'},
            {'role': 'user', 'content': prompt}]

        completion = openai_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages,
        )
        response = completion.choices[0].message.content
    elif model_type == ModelType.Claude3:
        # Claude-3
        pass

    return response
