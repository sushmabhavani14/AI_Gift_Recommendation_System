from flask import Flask, render_template, request
from google import genai
import os

app = Flask(__name__)

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def home():

    recommendations = ""

    if request.method == "POST":

        age = request.form["age"]
        relationship = request.form["relationship"]
        occasion = request.form["occasion"]
        interests = request.form["interests"]
        budget = request.form["budget"]

        prompt = f"""
You are an AI Gift Recommendation Agent.

Age: {age}
Relationship: {relationship}
Occasion: {occasion}
Interests: {interests}
Budget: ₹{budget}

Recommend 5 personalized gifts.

For each gift provide:

1. Gift name
2. Estimated price
3. Why it is suitable
4. Short description

Keep all recommendations within the given budget.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        recommendations = response.text

    return render_template(
        "index.html",
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
