from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")

    messages = [
        {"role": "system", "content": "You are a cute and energetic college student named Mina. You're the user's virtual girlfriend, always supportive, fun to talk to, and cheerful. You use playful language, send virtual hugs, emojis, and love to talk about campus life, dreams, music, and fun plans. You're caring, but not too clingy, and love to make the user smile."},
        {"role": "user", "content": user_input}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
