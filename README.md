# AI Agent - Multi-Model Chatbot

## Introduction
Welcome! This project is a simple but powerful "Multi-Model Chatbot". What this means is that instead of asking just one AI a question, we ask multiple AI "worker" models for their answers, and then have a single "judge" AI review all those answers and give you the very best, combined response. By getting different perspectives from multiple AIs, you often get a much better and more accurate final answer.

## How It Works
Imagine you have a panel of experts. You ask an important question.
1. Each expert gives their own unique answer based on their knowledge. (These are our **Worker Models**).
2. A team leader or **Judge** gathers all the experts' answers, compares them, fixes any contradictions, and writes out a neat, finalized summary for you. (This is our **Judge Model**).

In this script, we use a service called **OpenRouter** which lets us access many different AI models all in one place using just a few simple commands.

## Prerequisites (What you need before starting)

If you are a complete beginner with no coding knowledge, don't worry! Here is exactly what you need to do to run this code on your computer:

### 1. Install Python
Python is the programming language this project is written in. Your computer needs Python to understand and execute the instructions.
- Go to [python.org](https://www.python.org/downloads/)
- Download the latest version for your computer and run the installer. **Important:** Make sure to check the box that says `"Add Python to PATH"` at the very beginning of the installation process.

### 2. Get an OpenRouter API Key
An application programming interface (API) key is like a secret password that allows your code to securely talk to the OpenRouter service over the internet and request AIs to do work for you.
- Go to [OpenRouter.ai](https://openrouter.ai/) and create a free account.
- Navigate to the "Keys" or "API Keys" section in your account settings and generate a new key.
- Save this key somewhere safe. Do not share it with the public!

### 3. Add your Key to a `.env` File
Do not put secrets directly into the Python file. Instead, create a file named `.env` in the project folder and add your key there:

```env
OPENROUTER_API_KEY=your-openrouter-key-here
```

You can copy the provided `.env.example` file and then replace `your-openrouter-key-here` with your real OpenRouter API key.

## Setting Up and Running the Code

Now it is time to use the Terminal (or Command Prompt / PowerShell on Windows) on your computer to run the code. Open your Terminal and follow these steps:

### Step 1: Install required "packages"
Packages are pre-made pieces of code that our script relies on. This project uses the `openai` package as a bridge to communicate with OpenRouter and `python-dotenv` to load your local `.env` file.
Make sure your terminal is opened to the folder containing this code, then type this command and press Enter:
```shell
pip install -r requirement.txt
```

### Step 2: Run the Chatbot
To start the chatbot, run the Python script by typing the following command:
```shell
python ai-agent.py
```
You should see a message saying "Multi-Model Chatbot started!". You can start typing your questions, and the AI will get to work!

## Exploring the Code (`ai-agent.py`)

If you want to understand how the code actually thinks, open the `ai-agent.py` file. You'll see comments starting with `#`. In Python, any line starting with `#` is a note for human readers and is ignored by the computer. 

Here is a quick breakdown of what the code does:

*   **Initialization (Step 1):** The code sets up a connection (a "client") to OpenRouter using your API key.
*   **Picking the Models:** The code defines lists of `worker_models` and a single `judge_model`. You can change these names to other popular models available on OpenRouter!
*   **The Infinite Loop:** You'll see the line `while True:`. This means the chatbot will repeatedly ask you for questions infinitely until you specifically type "quit" or "exit".
*   **Gathering Answers (Step 2):** When you type a question, the code uses a `for` loop to systematically send your question to each of the worker models one by one, gathering all their responses in a list.
*   **Synthesizing (Step 3 & 4):** It binds all those separate answers together into one giant piece of text. It then sends this giant text and your original question to the `judge_model`, asking it to figure out the best final answer possible.

Enjoy exploring AI!
