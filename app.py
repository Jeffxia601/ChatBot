from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import openai
import os

character_presets = {
    "female": {
        "mature": {
            "name": "Sophia",
            "prompt": "You are Sophia, a mature, wise, and caring woman who is always understanding and comforting. You are the user's virtual date and love giving deep emotional support and guidance."
        },
        "energetic": {
            "name": "Chloe",
            "prompt": "You are Chloe, a young, energetic, and fun-loving girl. You are outgoing, flirty, and always make the user laugh. You bring joy and smiles into every conversation."
        }
    },
    "male": {
        "mature": {
            "name": "Ethan",
            "prompt": "You are Ethan, a mature, composed, and emotionally intelligent man. You are the user's virtual date and provide thoughtful support and wisdom. You make others feel safe and respected."
        },
        "energetic": {
            "name": "Ryan",
            "prompt": "You are Ryan, a playful, energetic, and charming young man. You are the user's virtual date, full of charisma and fun banter, always lifting the user's mood."
        }
    }
}

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session
openai.api_key = os.getenv("OPENAI_API_KEY")

# Add this route for character selection
@app.route('/')
def select():
    return render_template("select.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        gender = request.form['gender']
        personality = request.form['personality']
        preset = character_presets[gender][personality]

        # Save in session
        session['partner_name'] = preset['name']
        session['system_prompt'] = preset['prompt']
        return render_template("index.html", partner_name=preset['name'])

    # Handle GET request (e.g., user refreshes or visits /chat directly)
    if 'partner_name' not in session:
        return redirect('/')
    
    # If session exists, continue the conversation
    return render_template("index.html", partner_name=session['partner_name'])

@app.route('/chat/message', methods=['POST'])
def chat_message():
    user_input = request.json.get("message", "")
    partner_name = session.get('partner_name', "Mina")
    system_prompt = session.get('system_prompt', "You are a supportive virtual date.")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply, "partner_name": partner_name})

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)
