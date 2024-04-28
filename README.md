Hello! Welcome to the server side repository of Mood-Diary, a Voice-Based Mood Journaling application that incorporates the Nostr protocol for social features. To get started, see the section below. Note that for the emotion preditions to run correctly, you will need to run also the Python REST api backend, which you can find in the "python-ms" folder.

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

