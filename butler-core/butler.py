import ollama

def decide_function(ask):
    with open("document.md") as f:
        doc = f.read()
    prompt = f"""
        If my ask is: **{ask}**

        {doc}

        **You are to reply with a single JSON object describing the function call(s) needed to fulfill the user's request.

        Rules:
        - The response must be a single JSON object, not an array or multiple objects.
        - The JSON object must have two keys:
          - "function": the function name as a string.
          - "arguments": a dictionary of argument names and values needed for the function (empty if none).
        - If an argument is the result of another function, represent it as a nested JSON object in the same format.
        - If the user wants to perform multiple actions in sequence, always nest the function calls so that the output of one is used as the input to the next, and return only a single JSON object.
        - Do not return multiple JSON objects or arrays.
        - The response must start with '{' and end with '}'.
        Reply with only the JSON object, no extra text or formatting.**
    """

    response = ollama.chat(
        # model='qwen3:4b',
        # model='gemma3:latest',
        model='deepseek-r1:1.5b',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True
    )

    output = ""
    for chunk in response:
        if 'message' in chunk and 'content' in chunk['message']:
            print(chunk['message']['content'], end='', flush=True)
            output += chunk['message']['content']
    print()  # for newline after streaming
    return output.strip()