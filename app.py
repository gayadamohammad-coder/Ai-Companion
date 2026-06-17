from flask import Flask, render_template, request, jsonify
from src.memory import DatabaseManager
import ollama

app = Flask(__name__)
db = DatabaseManager()
db.create_tables()

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

@app.route("/")
def home():
    goals = db.get_goals()
    memories = db.get_memories()
    return render_template("index.html", goals=goals, memories=memories)

@app.route("/chat")
def chat_page():
    return render_template("chat.html")

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

    try:
        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[{"role": "system", "content": dynamic_prompt}] + history
        )
        ai_text = response["message"]["content"]
        history.append({"role": "assistant", "content": ai_text})
        return jsonify({"reply": ai_text, "history": history})

    except Exception as e:
        return jsonify({"reply": f"Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)