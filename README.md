# Thoth-Bot v1.3

Thoth-Bot is a powerful AI assistant and code generation tool that combines natural language processing capabilities with advanced coding functionalities. It offers a versatile command-line interface for chatting with AI, generating code, and managing AI agents.

![Thoth-Bot Screenshot](Animation.gif)

## Features

- **AI Chat**: Engage in conversations with an advanced AI model capable of answering questions and providing assistance on various topics.
- **Code Generation**: Automatically generate high-quality, well-structured Python code based on user instructions.
- **Code Improvement**: Analyze existing code, fix errors, and enhance functionality.
- **Multiple AI Models**: Choose from different AI models, including Llama 3.1, Gemini, and Groq, for various tasks.
- **Web UI Mode**: Launch a web-based user interface for enhanced interaction (in development).
- **Security Settings**: Adjustable security levels for Gemini models.

## Technologies Used

- Python
- asyncio
- Groq API
- Google Generative AI (Gemini)
- Rich (for console formatting)
- python-dotenv
- subprocess (for running generated code)

## Prerequisites

- Python 3.7 or later
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/thoth-bot.git
   cd thoth-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the main script:
   ```bash
   python main.py
   ```

## Usage

1. **Start the Bot**: Run `main.py` to launch Thoth-Bot.
2. **Choose a Mode**: Select from the following options:
   - **Chat**: Engage in a conversation with the AI.
   - **AI Coder**: Generate or improve Python code.
   - **Agents**: Manage AI agents (in development).
   - **Web UI**: Launch the web-based user interface (in development).
   - **Settings**: Configure your API keys.

3. **Select an AI Model**: Choose from Llama 3.1, Gemini, or Groq models.
4. **Interact**: Follow the prompts to chat, generate code, or perform other tasks.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Groq](https://groq.com/) for providing the AI API.
- [Google AI](https://ai.google/) for providing Gemini models.
- [Rich](https://github.com/Textualize/rich) for beautiful console formatting.
- [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variable management.

## Author

<p align="left">
<b>Umutcan Edizaslan:</b>
<a href="https://github.com/U-C4N" target="blank"><img align="center" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg" alt="TutTrue" height="30" width="40" /></a>
<a href="https://x.com/UEdizaslan" target="blank"><img align="center" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Twitter.svg" height="30" width="40" /></a>
</p>
