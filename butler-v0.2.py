import ollama

# STEP 1: Read transcript from file
with open("outputs-02/transcript.txt", "r") as f:
    transcript = f.read()

# STEP 2: Generate MoM + ToDos + Participants with Ollama local LLM
prompt = f"""
You are an AI assistant attending a meeting.

Based on the transcript below, generate the output in EXACTLY the following format:

[MoM] 
- A short summary of the meeting.

[ToDos] 
- Bullet points listing all the action items.
- For each action item, mention the person responsible.
- If any task is assigned to 'Shripal Mehta' (that's me), highlight it clearly with 🔴 at the beginning of the bullet point.

[Participants]
- List of all people who actively spoke in the meeting.

[Lead]
- Based on participation and context, who led or hosted the meeting.

Transcript:
\"\"\"
{transcript}
\"\"\"

IMPORTANT RULES:
- Do not skip any section.
- If any section has no information, write: 'None' or 'Not mentioned'.
- Keep the output strictly in the exact format above.
- VERY IMPORTANT: Carefully identify if any tasks are assigned to Shripal Mehta and highlight with 🔴.
"""

# response = ollama.chat(
#     model='phi3:mini',
#     messages=[{'role': 'user', 'content': prompt}]
# )

# response = ollama.chat(
#     model='mistral:7b',
#     messages=[{'role': 'user', 'content': prompt}]
# )

response = ollama.chat(
    model='llama3:8b',
    messages=[{'role': 'user', 'content': prompt}]
)

output = response['message']['content']

# STEP 3: Save output
with open("outputs-02/mom_todos.txt", "w") as f:
    f.write(output)

print("✅ MoM, ToDos, Participants & Lead generated. Check 'outputs-02/mom_todos.txt'")