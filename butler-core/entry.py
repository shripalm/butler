from oc import googleIt, searchIt
import datetime
from speakerMan import sayTheThing
from filerenamer import rename
from ytsubs import ytsubscaller
from butler import decide_function
from transcribe_audio import transcribe_audio
import json
import re


def greet():
    currHour = (datetime.datetime.now()).hour
    if currHour > 6 and currHour < 12:
        sayTheThing("Good Morning")
    elif currHour >= 12 and currHour < 5:
        sayTheThing("Good After Noon")
    elif currHour >= 5 and currHour < 8:
        sayTheThing("Good Evening")
    else:
        sayTheThing("Hope you had a great day")
    askforhelp('greet')


def farewell():
    currHour = (datetime.datetime.now()).hour
    if currHour > 6 and currHour < 12:
        sayTheThing("Have a good day")
    elif currHour >= 12 and currHour < 5:
        sayTheThing("Hope you have a great Noon")
    elif currHour >= 5 and currHour < 8:
        sayTheThing("Stay tight in eve")
    else:
        sayTheThing("Good Night")
    return 'farewell'


def extract_first_json(s):
    # Remove code block markers and whitespace
    s = s.strip()
    s = re.sub(r'^```json', '', s)
    s = re.sub(r'^```', '', s)
    s = s.strip('`\n ')
    match = re.search(r'({.*})', s, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No JSON object found in response")


def extract_last_json(s):
    # Remove code block markers and whitespace
    s = s.strip()
    s = re.sub(r'^```json', '', s)
    s = re.sub(r'^```', '', s)
    s = s.strip('`\n ')
    matches = list(re.finditer(r'({.*})', s, re.DOTALL))
    if matches:
        return matches[-1].group(1)
    raise ValueError("No JSON object found in response")

def removeThinking(s):
    # Remove <think>...</think> and <thinking>...</thinking> blocks (non-greedy)
    s = re.sub(r'<think>.*?</think>', '', s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r'<thinking>.*?</thinking>', '', s, flags=re.DOTALL | re.IGNORECASE)
    # Remove self-closing and empty tags
    s = re.sub(r'<think\s*/?>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'</think\s*>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'<thinking\s*/?>', '', s, flags=re.IGNORECASE)
    s = re.sub(r'</thinking\s*>', '', s, flags=re.IGNORECASE)
    return s.strip()

def askforhelp(fromFunc='indipendant'):
    sayTheThing('How May i help you?')
    task = input('At last we did ' + fromFunc + ', What Now: ')
    # Get function and arguments from decide_function
    raw_response = decide_function(task)
    try:
        removedThink = removeThinking(raw_response)
        jsonRes = extract_last_json(removedThink)
        print("Extracted JSON:", jsonRes)
        func_obj = json.loads(jsonRes)
    except Exception as e:
        print("Error parsing function call:", e)
        return
    print("Function call object:", func_obj)
    confirm = input("Do you want to execute this function call? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted by user.")
    else:
        response = execute_function_call(func_obj)
    if func_obj["function"] != 'farewell':
        askforhelp(func_obj["function"])

def execute_function_call(func_obj):
    func_name = func_obj["function"]
    arguments = {}
    for k, v in func_obj.get("arguments", {}).items():
        if isinstance(v, dict) and "function" in v:
            arguments[k] = execute_function_call(v)
        else:
            arguments[k] = v
    return eval(func_name)(**arguments)

def save_text(text, filename='output.txt'):
    with open(filename, 'w') as f:
        f.write(text)

# greet()
