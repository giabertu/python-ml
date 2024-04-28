Hello! Welcome to the server side repository of Mood-Diary, a Voice-Based Mood Journaling application that incorporates the Nostr protocol for social features. To get started, see the section below. Note that this is just the backend endpoint: to run the client, see the mood-diary folder


To run the server endpoint, you will need to create a .env file at the root level with a api key from OpenAI. See more infor [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key).

```bash
OPENAI_API_KEY=my-openai-key
```

## Installation

Before installing the project dependencies, it's recommended that you create a virtual environment. This ensures that the packages installed for this project do not interfere with other Python projects or system-wide Python packages.

### Setting up a Virtual Environment

For Unix/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

Then, install all depedencies by running:

```bash
pip install -r requirements.txt
```
Lastly, run the endpoint. Make sure your port 5000 is free. 

```bash
python index.py
```

