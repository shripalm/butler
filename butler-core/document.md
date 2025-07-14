# Butler Function Calling Protocol

This document describes the function calling protocol for the Butler program. Use this as a reference for LLMs to generate valid function call JSON objects.

## Function List

1. **farewell**
   - **Usage:** Exit, bye, or farewell tasks.
   - **Arguments:** None
   - **Example:**
     ```json
     {"function": "farewell", "arguments": {}}
     ```

2. **rename**
   - **Usage:** Rename files.
   - **Arguments:** (Specify as needed)
   - **Example:**
     ```json
     {"function": "rename", "arguments": {"old_name": "file1.txt", "new_name": "file2.txt"}}
     ```

3. **ytsubscaller**
   - **Usage:** Fetch YouTube captions.
   - **Arguments:** None
   - **Example:**
     ```json
     {"function": "ytsubscaller", "arguments": {}}
     ```

4. **googleIt**
   - **Usage:** Google something.
   - **Arguments:** (Specify as needed)
   - **Example:**
     ```json
     {"function": "googleIt", "arguments": {"query": "weather in Paris"}}
     ```

5. **transcribe_audio**
   - **Usage:** Transcribe audio from video.
   - **Arguments:**
     - `file_path` (required): Path to the video file.
     - `model_size` (optional): Model size to use.
   - **Example:**
     ```json
     {"function": "transcribe_audio", "arguments": {"file_path": "../discussion.mp4"}}
     ```
     ```json
     {"function": "transcribe_audio", "arguments": {"file_path": "../discussion.mp4", "model_size": "base"}}
     ```

6. **sayTheThing**
   - **Usage:** Speak something.
   - **Arguments:**
     - `text` (required): Text to speak. Can be a string or a nested function call.
     - `inpBool` (optional, boolean): Whether to take input after completion (default: false).
   - **Example:**
     ```json
     {"function": "sayTheThing", "arguments": {"text": "Hello!", "inpBool": false}}
     ```
     ```json
     {"function": "sayTheThing", "arguments": {"text": {"function": "transcribe_audio", "arguments": {"file_path": "../discussion.mp4"}}}}
     ```

7. **askforhelp**
   - **Usage:** Fallback for unrecognized tasks.
   - **Arguments:** None
   - **Example:**
     ```json
     {"function": "askforhelp", "arguments": {}}
     ```

8. **save_text**
   - **Usage:** Save text to a file.
   - **Arguments:**
     - `text` (required): Text to save. Can be a string or a nested function call.
     - `filename` (optional, default: 'output.txt'): Name of the file.
   - **Example:**
     ```json
     {"function": "save_text", "arguments": {"text": "Some text to save."}}
     ```
     ```json
     {"function": "save_text", "arguments": {"text": {"function": "transcribe_audio", "arguments": {"file_path": "../discussion.mp4"}}, "filename": "output.txt"}}
     ```

## Multiple Actions (Nesting)

- To perform multiple actions in sequence, always nest the function calls so that the output of one is used as the input to the next. Only return a single JSON object.
- **Example:** Transcribe audio and then save the result:
  ```json
  {"function": "save_text", "arguments": {"text": {"function": "transcribe_audio", "arguments": {"file_path": "../discussion.mp4"}}, "filename": "output.txt"}}
  ```
- **Example:** Fetch YouTube captions and speak them:
  ```json
  {"function": "sayTheThing", "arguments": {"text": {"function": "ytsubscaller", "arguments": {}}}}
  ```

## Output Format
- All JSON keys and string values must be enclosed in double quotes (").
- Do not include any comments, explanations, or extra text.
- Only return a single valid JSON object, and nothing else.
- The response must start with '{' and end with '}'.
