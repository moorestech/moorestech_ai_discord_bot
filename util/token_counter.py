import tiktoken

encoder = tiktoken.encoding_for_model("gpt-3.5-turbo")


def get_token_count(content):
    return len(encoder.encode(content))
