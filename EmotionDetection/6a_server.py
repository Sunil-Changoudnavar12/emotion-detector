"""Flask application for the IBM emotion detection demo."""

from flask import Flask, render_template_string, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Emotion Detector</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        background: linear-gradient(135deg, #f5f7ff, #eef2ff);
        color: #1f2937;
      }
      .container {
        max-width: 700px;
        margin: 60px auto;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.12);
        padding: 30px;
      }
      h1 {
        color: #312e81;
        margin-bottom: 20px;
      }
      form {
        display: flex;
        flex-direction: column;
        gap: 14px;
      }
      textarea {
        width: 100%;
        min-height: 120px;
        padding: 12px;
        border: 1px solid #c7d2fe;
        border-radius: 10px;
        font-size: 16px;
        box-sizing: border-box;
      }
      button {
        padding: 12px 18px;
        border: none;
        border-radius: 10px;
        background: #4f46e5;
        color: white;
        font-size: 16px;
        cursor: pointer;
      }
      button:hover {
        background: #4338ca;
      }
      .error {
        background: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 12px;
      }
      .result {
        margin-top: 24px;
        background: #f8fafc;
        border: 1px solid #dbeafe;
        border-radius: 12px;
        padding: 18px;
      }
      .emotion-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 12px;
      }
      .emotion-table th, .emotion-table td {
        text-align: left;
        padding: 8px 10px;
        border-bottom: 1px solid #e5e7eb;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Emotion Detector</h1>
      <form method="post">
        <label for="text">Enter text to analyze:</label>
        <textarea id="text" name="text" placeholder="Type a sentence here...">{{ input_text }}</textarea>
        <button type="submit">Analyze emotion</button>
      </form>

      {% if error %}
        <div class="error">
          <strong>Error:</strong> {{ error }}
        </div>
      {% endif %}

      {% if result %}
        <div class="result">
          <h2>Result</h2>
          <p><strong>Dominant emotion:</strong> {{ result['dominant_emotion'] }}</p>
          <table class="emotion-table">
            <tr><th>Emotion</th><th>Score</th></tr>
            <tr><td>Anger</td><td>{{ result['anger'] }}</td></tr>
            <tr><td>Disgust</td><td>{{ result['disgust'] }}</td></tr>
            <tr><td>Fear</td><td>{{ result['fear'] }}</td></tr>
            <tr><td>Joy</td><td>{{ result['joy'] }}</td></tr>
            <tr><td>Sadness</td><td>{{ result['sadness'] }}</td></tr>
          </table>
        </div>
      {% endif %}
    </div>
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the home page and handle text submission."""
    error = ""
    result = None
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("text", "")
        if not input_text or not input_text.strip():
            error = "Please enter some text before analyzing the emotion."
        else:
            result = emotion_detector(input_text)

    return render_template_string(HTML_TEMPLATE, error=error, result=result, input_text=input_text)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
