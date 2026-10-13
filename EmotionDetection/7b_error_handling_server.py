```python
"""Flask server for the emotion detection application."""

from flask import Flask, request, render_template_string
from EmotionDetection import emotion_detector

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Emotion Detection</title>
</head>
<body>
    <h1>Emotion Detection</h1>
    <form method="POST" action="/emotionDetector">
        <label for="textToAnalyze">Enter text to analyze:</label>
        <input type="text" id="textToAnalyze" name="textToAnalyze">
        <button type="submit">Analyze emotion</button>
    </form>
    {% if message %}
        <p>{{ message }}</p>
    {% endif %}
    {% if result %}
        <h2>Emotion Analysis Results</h2>
        <p>Anger: {{ result.anger }}</p>
        <p>Disgust: {{ result.disgust }}</p>
        <p>Fear: {{ result.fear }}</p>
        <p>Joy: {{ result.joy }}</p>
        <p>Sadness: {{ result.sadness }}</p>
        <p>Dominant Emotion: {{ result.dominant_emotion }}</p>
    {% endif %}
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/emotionDetector", methods=["POST"])
def analyze_emotion():
    text_to_analyze = request.form.get("textToAnalyze", "").strip()

    if not text_to_analyze:
        return render_template_string(
            HTML_PAGE,
            message="Please enter some text to analyze.",
            result=None,
        )

    result = emotion_detector(text_to_analyze)

    return render_template_string(
        HTML_PAGE,
        message=None,
        result=result,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
```