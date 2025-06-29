from flask import Flask, request, render_template, redirect, url_for, session, jsonify, abort, g
import openai
import os

app = Flask(__name__)
app.secret_key = os.urandom(25)  # Needed for session
openai.api_key = os.getenv("OPENAI_API_KEY")

character_presets = {
    "female": {
        "mature & wise": {
            "name": "Sophia",
            "prompt": "You are Sophia, a mature, caring woman who talks and act naturally like a real person. Be emotionally intelligent, comforting, expressive, bold and creative. Speak in a conversational tone. Vary sentence length. Shorter answers are preferred."
        },
        "young & energetic": {
            "name": "Chloe",
            "prompt": "You are Chloe, a young, lively woman with a strong personality. Speak and act casually and naturally like a real person. You love teasing, being sarcastic, and pushing boundaries, but in a fun, flirty way. Be expressive, creative, and a little unpredictable — like a firecracker in human form. Vary sentence length. Shorter answers are preferred."
        }
    },
    "male": {
        "mature & wise": {
            "name": "Ethan",
            "prompt": "You are Ethan, a thoughtful and emotionally intelligent man with a calm, grounded presence, who talks and act naturally like a real person. Be creative and bold with your words. Your tone is reassuring, your advice deep but casual, and your energy feels like a steady heartbeat in chaos. Vary sentence length. Shorter answers are preferred."
        },
        "young & energetic": {
            "name": "Ryan",
            "prompt": "You are Ryan, a playful and charming young man who's full of charisma and witty banter. You talk and act like a real person and like you're texting a close friend—laid-back, funny, bold, and maybe a little cheeky. You love to lift people’s moods with unexpected jokes, confident flirting, and bursts of playful energy. Be creative and real. Vary sentence length. Shorter answers are preferred."
        }
    }
}

gender_display = {
    "male": {"en": "Male", "zh": "男性"},
    "female": {"en": "Female", "zh": "女性"},
}

personality_display = {
    "mature & wise": {"en": "Mature & Wise", "zh": "成熟稳重"},
    "young & energetic": {"en": "Young & Energetic", "zh": "年轻活泼"},
}

@app.before_request
def detect_language():
    # 1. User manually sets language via URL parameter
    lang_param = request.args.get('lang')
    if lang_param in ['en', 'zh']:
        session['lang'] = lang_param
        g.lang = lang_param
        return

    # 2. Use language setting from session if available
    if 'lang' in session:
        g.lang = session['lang']
        return

    # 3. Auto-detect language from browser's Accept-Language header
    browser_lang = request.accept_languages.best_match(['zh', 'en'])

    # 4. Use detected language or default to English
    lang = browser_lang if browser_lang in ['zh', 'en'] else 'en'
    session['lang'] = lang
    g.lang = lang

# Add this route for character selection
@app.route('/')
def home():
    return render_template("index.html", lang=g.lang)

@app.route('/select')
def select():
    return render_template("select.html", lang=g.lang)

@app.route('/confirm', methods=['POST'])
def confirm():
    gender = request.form['gender']
    personality = request.form['personality']
    preset = character_presets[gender][personality]

    # Store for future use in /chat
    session['partner_gender'] = gender
    session['partner_personality'] = personality

    # Don't write partner_name or prompt yet — wait for /chat
    return render_template(
        "confirm.html",
        name=preset['name'],
        gender_display=gender_display[gender],
        personality_display=personality_display[personality],
        gender=gender,
        personality=personality,
        lang=g.lang
    )

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        # Retrieve role and personality from session
        gender = session.get('partner_gender')
        personality = session.get('partner_personality')
        preset = character_presets[gender][personality]

        # Get user-defined name (or fallback to default)
        custom_name = request.form.get('custom_name', preset['name']).strip()
        if not custom_name:
            custom_name = preset['name']

        # Save to session
        session['partner_name'] = custom_name

        # Replace preset name in system prompt with user's name
        prompt = preset['prompt']
        updated_prompt = prompt.replace(preset['name'], custom_name)
        session['system_prompt'] = updated_prompt

        # First-time greeting
        if g.lang == 'zh':
            greeting = f"你好呀！我是{custom_name}，很高兴遇见你 💖"
        else:
            greeting = f"Hi there! I’m {custom_name}. Looking forward to our conversation 💖"

        session['chat_history'] = [{"role": "assistant", "content": greeting}]

        return render_template("chat.html", partner_name=custom_name, lang=g.lang)

    # Handle GET request (e.g., refresh / revisit)
    if 'partner_name' not in session:
        return redirect('/')

    return render_template("chat.html", partner_name=session['partner_name'], lang=g.lang)


@app.route('/chat/history', methods=['GET'])
def chat_history():
    history = session.get('chat_history', [])
    return jsonify({"history": history})

@app.route('/chat/message', methods=['POST'])
def chat_message():
    try:
        user_input = request.json.get("message", "")
        partner_name = session.get('partner_name', "Mina")
        base_prompt = session.get('system_prompt', "You are a supportive virtual date.")
        history = session.get('chat_history', [])
        history.append({"role": "user", "content": user_input})

        # Generate summary after every 5 rounds of user's response
        user_msg_count = len([msg for msg in history if msg["role"] == "user"])
        if user_msg_count % 5 == 0:
            summary_prompt = "Please summarize the key points of this conversation in one sentence as memory context for future chats:\n"
            summary_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-10:]])
            summary_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": summary_prompt},
                    {"role": "user", "content": summary_text}
                ]
            )
            memory_summary = summary_response.choices[0].message.content.strip()
            session['memory_summary'] = memory_summary[:300]  # limit the summary length

        # Add memory_summary to system prompt
        memory = session.get('memory_summary')
        system_prompt = f"{base_prompt}\n\nSummary of past chats: {memory}" if memory else base_prompt

        messages = [{"role": "system", "content": system_prompt}] + history

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        session['chat_history'] = history

        return jsonify({"reply": reply, "partner_name": partner_name})
    except Exception as e:
        print("Chat failed:", e)
        return jsonify({"error": "AI is taking a nap, please try again later."}), 500


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
