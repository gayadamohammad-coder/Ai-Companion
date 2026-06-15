from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>AI Companion</h1>
    <p>Welcome Mohammed!</p>
    """

if __name__ == "__main__":
    app.run(debug=True)