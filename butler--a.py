import whisper
import ollama

# STEP 1: Transcribe
model = whisper.load_model("base")
result = model.transcribe("discussion.mp4")
transcript = result['text']

# Optional: save transcript
with open("outputs/transcript.txt", "w") as f:
    f.write(transcript)

# STEP 2: Generate MoM + ToDos with Ollama local LLM
prompt = f"""
You are an AI assistant attending a meeting.

From the following transcript, generate:

[MoM] 
- A short summary of the meeting

[ToDos] 
- Bullet points listing all the action items.

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

response = ollama.chat(
    model='phi3:mini',
    messages=[{'role': 'user', 'content': prompt}]
)

output = response['message']['content']

# STEP 3: Save output
with open("outputs/mom_todos.txt", "w") as f:
    f.write(output)

print("✅ MoM & ToDos generated. Check 'outputs/mom_todos.txt'")