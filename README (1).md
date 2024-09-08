
# PyBot: Your Python Coding Assistant 🐍

PyBot is an AI-powered assistant designed to help you with Python-related coding questions. Whether you're a beginner or an experienced developer, PyBot is here to assist with syntax, code optimization, best practices, library usage, debugging tips, and more.

## Features

- **Interactive Chat**: Ask any Python-related question and get instant responses.
- **Code Formatting**: The assistant provides properly formatted and indented code snippets.
- **Multiple LLM Providers**: Choose from various language models like OpenAI's GPT-3.5, GPT-4, and Anthropic's Claude-3.
- **Background Customization**: Set a custom background image to enhance the look and feel of the application.
- **Responsive Design**: The application is built using Streamlit and is optimized for different screen sizes.
- **Copy Code to Clipboard**: Easily copy the code snippets provided by PyBot with a single click.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Streamlit
- `notdiamond` library (for managing LLM models)
- Environment variables for API keys

### Step-by-Step Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/pybot.git
   cd pybot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the root of your project and add the following:

   ```env
   NOTDIAMOND_API_KEY=your_notdiamond_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   Open your web browser and navigate to `http://localhost:8501` to start using PyBot.

## Customization

### Background Image

You can change the background image by replacing the `bg.avif` file in the project directory.

### LLM Providers

You can modify or add more language models to the `llm_providers` list in the `app.py` file.

## Usage

- **Ask a Question**: Type your Python-related question in the input box at the bottom and hit Enter.
- **Select LLM Provider**: Use the sidebar to switch between different language models for your queries.
- **Copy Code**: Hover over the code snippet to see a "Copy" button. Click it to copy the code to your clipboard.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [NotDiamond](https://notdiamond.com)
- [OpenRouter](https://openrouter.ai)
```

You can replace `"yourusername/pybot.git"` with the actual repository URL if you decide to publish it.
## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    