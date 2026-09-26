# Emotion Detector

This project is a beginner-friendly Flask application that analyzes text and detects the dominant emotion using IBM Watson Natural Language Understanding.

## Project purpose

The application accepts a sentence, detects whether it is primarily expressing anger, disgust, fear, joy, or sadness, and displays the score for each emotion along with the dominant emotion.

## Project structure

```text
Emotion-Detector/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── test_emotion_detection.py
├── server.py
├── README.md
├── requirements.txt
├── .gitignore
└── screenshots/
```

## Setup

Open a terminal in the project folder and run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Flask app

```bash
python server.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Run the unit tests

```bash
python -m unittest test_emotion_detection.py
```

## Run pylint

```bash
pylint server.py
```

## GitHub-ready repository commands

```bash
git init
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/Emotion-Detector.git
git push -u origin main
```

## Environment variables for Watson

This project supports optional IBM Watson credentials:

```bash
export WATSON_API_KEY="your_api_key"
export WATSON_URL="https://your-service-url"
```

On Windows PowerShell:

```powershell
$env:WATSON_API_KEY="your_api_key"
$env:WATSON_URL="https://your-service-url"
```

If the credentials are not configured, the application falls back to a built-in keyword-based emotion model so the project remains runnable for learning and testing.
