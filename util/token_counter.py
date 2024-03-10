import tiktoken

encoder = tiktoken.encoding_for_model("gpt2")


def get_token_count(content):
    return len(encoder.encode(content))
