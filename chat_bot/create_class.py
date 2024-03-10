from util import embedding
from util import query_ai

system_prompt = 'This is part of the moorestech code. Please refer to this and follow the instructions.\n'

user_request = """
As a senior C# programmer, you will help develop the automated industrial game "moorestech".
The code we need you to write this time is code related to adding the definition of veins to the Map definition, and adding the functionality to allow the mining machine to mine those veins.
Please write a test code that enables the miner to mine the veins defined in the Map, referring to the test code for the miner so far.
When writing the code, do not write it in parts, but write the entire code.

"""

rag_prompt = embedding.create_rag_prompt(user_request, token_limit=30000)

prompt = system_prompt + rag_prompt + "\n" + user_request

print(prompt)

print(query_ai.query_ai(prompt, query_ai.ModelType.GPT4))


