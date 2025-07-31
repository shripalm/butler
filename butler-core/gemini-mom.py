import requests
# import sayTheThing from sharkSon.speakerMan
from speakerMan import sayTheThing
from entry import save_text


with open("../transcripts/dentsu-spark-multi-tenancy.txt", "r") as f:
    transcript = f.read()

# STEP 2: Generate MoM + ToDos + Participants with Ollama local LLM
prompt = f"""
You are an AI assistant attending a meeting.

Based on the transcript below, generate the output in EXACTLY the following format:

[M.O.M] 
- A summary of the meeting.
- Important things discussed.

Transcript:
\"\"\"
{transcript}
\"\"\"

"""

class GeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Updated to v1beta endpoint and gemini-2.0-flash model as per provided curl
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.headers = {"Content-Type": "application/json"}

    def chat(self, prompt: str) -> str:
        url = f"{self.base_url}?key={self.api_key}"
        data = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        response = requests.post(url, json=data, headers=self.headers)
        if not response.ok:
            try:
                error_info = response.json()
                return f"[HTTP {response.status_code}] {error_info.get('error', {}).get('message', 'Unknown error')}"
            except Exception:
                return f"[HTTP {response.status_code}] {response.text}"
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return f"[Error: Unexpected response format] {result}"

    def list_models(self):
        url = f"https://generativelanguage.googleapis.com/v1/models?key={self.api_key}"
        response = requests.get(url, headers=self.headers)
        if not response.ok:
            try:
                error_info = response.json()
                print(f"[HTTP {response.status_code}] {error_info.get('error', {}).get('message', 'Unknown error')}")
            except Exception:
                print(f"[HTTP {response.status_code}] {response.text}")
            return
        result = response.json()
        print("Available models:")
        for model in result.get("models", []):
            print(f"- {model.get('name')}")

# Example usage:
client = GeminiClient("AIzaSyAW3bf6TFoHUjXQoaUMubn1y3dyLejhgZA")
op = client.chat(prompt)
# sayTheThing(op)
save_text(op, '../mom/dentsu-spark-multi-tenancy.md')
print(client.list_models())