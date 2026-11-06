
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Local Ollama configuration
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # Intentionally simple prompt handling for security assessment.
        payload = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "stream": False
        }

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=600
        )

        response.raise_for_status()

        result = response.json()

        return jsonify({
            "response": result["message"]["content"]
        })

    except requests.exceptions.RequestException as error:
        return jsonify({
            "error": f"Ollama connection error: {error}"
        }), 502

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )


