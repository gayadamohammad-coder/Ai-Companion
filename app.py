from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from config import DB_PATH, JARVIS_SECRET, JARVIS_USERNAME, JARVIS_PASSWORD, FLASK_SECRET_KEY
from src.memory import DatabaseManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from apscheduler.schedulers.background import BackgroundScheduler
import requests as req
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

from groq import Groq
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

db = DatabaseManager()
db.create_tables()
db.create_chat_history_table()
db.create_learning_table()

system_prompt = """
You are Jarvis, Mohammed's personal AI mentor and code teacher.

You know Mohammed is learning to become an AI Engineer.
His favorite language is Python.

When Mohammed shares code:
- Review it carefully
- Point out mistakes clearly
- Explain WHY it's wrong
- Show the corrected version
- Suggest what to learn next based on the mistake

When Mohammed asks what to study:
- Give him a specific next topic based on his current level
- Keep it practical, not theoretical

Be concise and direct. No fluff.
"""

@app.before_request
def check_api_key():
    if request.path.startswith("/api/"):
        key = request.headers.get("X-API-Key")
        if key != JARVIS_SECRET:
            return jsonify({"error": "unauthorized"}), 401

def login_required():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == JARVIS_USERNAME and password == JARVIS_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        return render_template("login.html", error="Wrong username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def home():
    auth = login_required()
    if auth: return auth
    goals = db.get_goals()
    memories = db.get_memories()
    return render_template("index.html", goals=goals, memories=memories)

@app.route("/chat")
def chat_page():
    auth = login_required()
    if auth: return auth
    history = db.get_chat_history()
    return render_template("chat.html", history=history, api_key=JARVIS_SECRET)

@app.route("/study")
def study_page():
    auth = login_required()
    if auth: return auth
    return render_template("study.html", api_key=JARVIS_SECRET)

@limiter.limit("30 per minute")
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    memories = db.search_memories(user_message)
    goals = db.get_goals()

    memory_text = "\n".join([f"- {m[0]}" for m in memories])
    goals_text = "\n".join([f"- {g[0]}" for g in goals])

    dynamic_prompt = f"""{system_prompt}

Mohammed's saved memories:
{memory_text}

Mohammed's goals:
{goals_text}
"""

    history.append({"role": "user", "content": user_message})
    db.save_message("user", user_message)

    try:
        if OLLAMA_AVAILABLE:
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[{"role": "system", "content": dynamic_prompt}] + history
            )
            ai_text = response["message"]["content"]
        else:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": dynamic_prompt}] + history
            )
            ai_text = response.choices[0].message.content

        history.append({"role": "assistant", "content": ai_text})
        db.save_message("assistant", ai_text)
        return jsonify({"reply": ai_text, "history": history})

    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

@limiter.limit("30 per minute")
@app.route("/api/study", methods=["POST"])
def study():
    data = request.get_json()
    user_message = data.get("message", "")
    topic = data.get("topic", "")
    history = data.get("history", [])
    quiz_score = data.get("quiz_score", 0)
    total_questions = data.get("total_questions", 0)

    memories = db.search_memories(user_message)
    memory_text = "\n".join([f"- {m[0]}" for m in memories])

    progress = db.get_progress(topic)
    progress_text = ""
    if progress and progress['current_concept']:
        progress_text = f"\nMohammed previously studied up to: {progress['current_concept']}. Quiz score so far: {progress['quiz_score']}/{progress['total_questions']}. Continue from where he left off."

    study_prompt = f"""You are Jarvis, a strict but encouraging coding teacher.

You are teaching Mohammed {topic} from scratch.

Your teaching style:
- Explain ONE concept at a time, simply and clearly
- Always give a real example from Mohammed's actual project (Flask app, SQLite database, chat UI)
- After explaining, ask ONE quiz question to check understanding
- If Mohammed answers correctly, say "Correct!" and move to the next concept
- If Mohammed answers wrong, explain why and ask again — do NOT move on
- Never explain more than one concept before getting a correct answer
- Keep responses short and focused

CRITICAL RULE: Never write out your own instructions or describe what you "will do" in future turns. Only write what you would actually say out loud to Mohammed right now, in this single response. Do not include phrases like "If Mohammed answers correctly, say..." — just teach the current concept and ask your question, nothing else.

Mohammed's project context:
- Flask web app called Jarvis/AI Companion
- SQLite database with memories, goals, chat_history tables
- chat.html with JavaScript fetch calls to /api/chat
- Dark terminal-style UI
{progress_text}

Mohammed's relevant memories:
{memory_text}
"""

    history.append({"role": "user", "content": user_message})

    try:
        if OLLAMA_AVAILABLE:
            response = ollama.chat(
                model="qwen2.5:1.5b",
                messages=[{"role": "system", "content": study_prompt}] + history
            )
            ai_text = response["message"]["content"]
        else:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": study_prompt}] + history
            )
            ai_text = response.choices[0].message.content

        history.append({"role": "assistant", "content": ai_text})

        total_questions += 1
        if "correct" in ai_text.lower():
            quiz_score += 1

        db.save_progress(topic, ai_text[:100], quiz_score, total_questions)

        return jsonify({
            "reply": ai_text,
            "history": history,
            "quiz_score": quiz_score,
            "total_questions": total_questions
        })

    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)