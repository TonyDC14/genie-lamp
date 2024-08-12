# src/utils.py

def split_prompt(prompt, max_length):
    """
    Utility function to split a prompt into chunks of a specified maximum length.
    """
    return [prompt[i:i + max_length] for i in range(0, len(prompt), max_length)]
