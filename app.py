from flask import Flask, render_template, request, jsonify
from src.memory import DatabaseManager
import ollama

app = Flask(__name__)
db = DatabaseManager()
db.create_tables()
db.create_chat_history_table()

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

@app.route("/study")
def study_page():
    return render_template("study.html")

@app.route("/")
def home():
    goals = db.get_goals()
    memories = db.get_memories()
    return render_template("index.html", goals=goals, memories=memories)

@app.route("/chat")
def chat_page():
    history = db.get_chat_history()
    return render_template("chat.html", history=history)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    history = data.get("history", [])

    memories = db.get_memories()
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
        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[{"role": "system", "content": dynamic_prompt}] + history
        )
        ai_text = response["message"]["content"]
        history.append({"role": "assistant", "content": ai_text})
        db.save_message("assistant", ai_text)
        return jsonify({"reply": ai_text, "history": history})

    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500
    

@app.route("/api/study", methods=["POST"])
def study():
    data = request.get_json()
    user_message = data.get("message", "")
    topic = data.get("topic", "")
    history = data.get("history", [])

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

Mohammed's project context:
- Flask web app called Jarvis/AI Companion
- SQLite database with memories, goals, chat_history tables
- chat.html with JavaScript fetch calls to /api/chat
- Dark terminal-style UI

Start by introducing the first concept for {topic}. Do not ask what they want to learn — just start teaching.
"""

    history.append({"role": "user", "content": user_message})

    try:
        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[{"role": "system", "content": study_prompt}] + history
        )
        ai_text = response["message"]["content"]
        history.append({"role": "assistant", "content": ai_text})
        return jsonify({"reply": ai_text, "history": history})
    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)