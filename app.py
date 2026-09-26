from flask import Flask, render_template, request
from google import genai
from google.genai import types
import os
import json

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = []

    if request.method == "POST":

        age = request.form["age"]
        relationship = request.form["relationship"]
        occasion = request.form["occasion"]
        interests = request.form["interests"]
        budget = request.form["budget"]

        prompt = f"""
You are an AI Gift Recommendation Agent.

User details:
Age: {age}
Relationship: {relationship}
Occasion: {occasion}
Interests: {interests}
Budget: ₹{budget}

Recommend exactly 5 personalized gifts.

IMPORTANT:
- Keep every gift within the given budget.
- Give realistic estimated prices in Indian Rupees.
- Return ONLY valid JSON.
- Do not use Markdown.
- Do not use ###, **, bullets or ---.

Use exactly this JSON format:

[
  {{
    "name": "Gift name",
    "price": "₹1,500",
    "why": "Short reason why this gift is suitable",
    "description": "Short description of the gift"
  }}
]
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        try:
            recommendations = json.loads(response.text)
        except:
            recommendations = []

    return render_template(
        "index.html",
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
