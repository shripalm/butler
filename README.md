# Butler

## Overview

**Butler** is an intelligent personal assistant project built primarily with Python, designed to interact with users through natural language. Leveraging a suite of powerful AI and machine learning libraries, Butler aims to provide a comprehensive conversational experience, integrating capabilities such as speech processing, web information retrieval, and potentially deep system-level interactions on macOS. The project structure suggests a core Python backend with a dedicated user interface component (`bot-ui`).

## Features

*   **AI-Powered Conversations**: Utilizes advanced language models from OpenAI and Ollama for understanding and generating human-like text, enabling dynamic and intelligent interactions.
*   **Speech-to-Text Transcription**: Integrates OpenAI Whisper for highly accurate audio transcription, allowing users to interact with Butler using voice commands and input.
*   **Text-to-Speech Generation**: Employs `pyttsx3` and `gtts` (Google Text-to-Speech) to provide vocal responses, making the assistant's interactions more natural and accessible.
*   **Web Search Integration**: Capable of performing real-time web searches using `googlesearch-python` to fetch up-to-date information and answer queries.
*   **YouTube Transcript Fetching**: Can retrieve transcripts from YouTube videos, enabling content analysis, summarization, or specific information extraction.
*   **Web Content Parsing**: Uses `BeautifulSoup4` for parsing HTML content, likely for extracting structured data or specific information from web pages.
*   **macOS System Integration**: Extensive use of `pyobjc` frameworks suggests potential for deep integration with macOS services and applications, offering system control, automation, or information retrieval specific to the Apple ecosystem.
*   **Robust Data Processing**: Leverages `NumPy`, `Numba`, and `PyTorch` for efficient numerical operations, data manipulation, and machine learning tasks.

## Tech Stack

**Primary Language:**
*   Python

**Key Libraries & Tools:**
*   **AI/ML/NLP**: `openai`, `ollama`, `openai-whisper`, `torch`, `numpy`, `numba`, `tiktoken`
*   **Web/Networking**: `httpx`, `requests`, `beautifulsoup4`, `googlesearch-python`, `youtube-transcript-api`
*   **Audio/Video**: `pyttsx3`, `gtts`, `moviepy`, `pillow`
*   **System Integration (macOS)**: `pyobjc` (and numerous `pyobjc-framework-*` packages)
*   **Data Validation**: `pydantic`
*   **Templating**: `Jinja2`
*   **Utilities**: `tqdm`, `filelock`, `fsspec`, `distro`, `regex`

## Installation

To set up and run Butler on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/shripalm/butler.git # Replace with actual repo URL
    cd butler
    ```

2.  **Set up Python Environment:**
    It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` includes a large number of `pyobjc-framework-*` packages, indicating that full functionality is likely dependent on a macOS environment.*

4.  **Ollama Setup (if applicable):**
    If you plan to use Ollama for local language models, ensure you have the Ollama server installed and running, and the necessary models downloaded. Refer to the [Ollama documentation](https://ollama.com/docs) for detailed instructions.

5.  **Bot UI Setup (if applicable):**
    The `bot-ui` directory contains a `package.json` file, suggesting a separate JavaScript-based frontend application. If this is the case, navigate into the directory and install its dependencies:
    ```bash
    cd bot-ui
    npm install # Or `yarn install`, depending on your package manager
    cd .. # Return to the root directory
    ```

## Environment Variables

No specific environment variables were explicitly detected in the repository analysis. However, for the project to function correctly, you will likely need to configure API keys for external services:

*   **`OPENAI_API_KEY`**: Your API key for accessing OpenAI services.
    ```
    OPENAI_API_KEY="sk-your_openai_api_key_here"
    ```
*   Other API keys might be required depending on specific integrations or future features.

It is recommended to manage these securely using a `.env` file and a library like `python-dotenv`.

## API Endpoints

No internal API endpoints were explicitly detected within the analyzed files. The project primarily interacts with several external APIs for its core functionalities:

*   **OpenAI API**: For advanced language model interactions.
*   **Ollama API**: For local large language model interactions.
*   **Google Search API (via `googlesearch-python`)**: For performing web search queries.
*   **YouTube Data API (via `youtube-transcript-api`)**: For fetching video transcripts.

## Folder Structure

The repository has the following detected top-level structure:

```
.
├── README.md               # This README file
├── requirements.txt        # Python dependency list
└── bot-ui/                 # Directory for the user interface component
    ├── README.md           # README specific to the bot UI
    └── package.json        # Node.js package manifest for the UI
```

The core Python logic for the "Butler" assistant is expected to reside in other Python files within the root directory or subdirectories not explicitly listed in the metadata but implied by the `requirements.txt` dependencies.

## Scripts

No specific executable scripts were explicitly detected in the metadata. To run the Butler assistant, you would typically execute a main Python file:

```bash
python main.py # Or whatever your main entry point file is named (e.g., `app.py`, `run.py`)
```

If the `bot-ui` is a separate application, it would have its own run command:

```bash
cd bot-ui
npm start # Or `yarn start`, etc., depending on the UI's configuration
```

## Deployment

Butler is primarily designed for local deployment as a personal assistant.

*   **Local Machine**: After following the installation steps, run the Python backend and the `bot-ui` (if separate) directly on your computer.
*   **Containerization (e.g., Docker)**: For easier setup, dependency management, and portability, consider containerizing the Python application using Docker. This would involve creating a `Dockerfile` to build an image that includes all Python dependencies and potentially the `bot-ui`.

## Future Improvements

*   **Enhanced NLP Capabilities**: Integrate more sophisticated natural language understanding (NLU) and natural language generation (NLG) techniques for even more nuanced and context-aware conversations.
*   **Broader Service Integrations**: Expand connectivity to a wider range of third-party services, smart home devices, productivity tools (e.g., calendar, email), or custom APIs.
*   **Modular Plugin Architecture**: Develop a flexible plugin system to allow users or developers to easily extend Butler's capabilities with new features and integrations.
*   **Cross-Platform UI**: If the current `bot-ui` is platform-specific, explore options for a truly cross-platform desktop application (e.g., using Electron, PyQt, or a web-based interface) to reach a wider audience.
*   **Voice Activity Detection (VAD)**: Implement VAD for more efficient and natural voice interaction, ensuring the assistant only processes speech when actively spoken to.
*   **Memory and Context Management**: Improve the assistant's ability to remember past conversations and maintain context over longer interactions, leading to more coherent dialogues.

## License

This project is licensed under the MIT License. Please see the `LICENSE` file (if present) in the repository for full details.