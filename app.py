from flask import Flask, request, render_template, jsonify
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# ----------------------------
# Model Initialization
# ----------------------------
def get_model():
    """Automatically pick best available Gemini model"""
    preferred_models = [
        "gemini-2.5-flash",
        "gemini-1.5-flash"
    ]
    
    for model_name in preferred_models:
        try:
            print(f"🔹 Attempting to use model: {model_name}")
            model = genai.GenerativeModel(model_name)
            print(f"✅ Model ready: {model_name}")
            return model
        except Exception as e:
            print(f"⚠️ Could not load {model_name}: {e}")
            continue

    raise RuntimeError("No Gemini models could be loaded. Check your API key!")

# Initialize model once at startup
model = get_model()

# Ensure feedback directory exists
os.makedirs("feedback", exist_ok=True)

# ----------------------------
# Helper functions
# ----------------------------
def answer_question(question):
    prompt = f"Answer this question clearly and concisely: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def summarize_text(text):
    prompt = f"Summarize the following text with bullet points:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def generate_creative_content(prompt_text):
    if any(word in prompt_text.lower() for word in ["story", "tale", "narrative"]):
        prompt = f"Write a short story (200-300 words) about: {prompt_text}"
    elif any(word in prompt_text.lower() for word in ["poem", "poetry", "verse"]):
        prompt = f"Write a creative poem about: {prompt_text}"
    else:
        prompt = f"Generate creative content about: {prompt_text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating creative content: {str(e)}"

def save_feedback(function_type, query, response, helpful):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("feedback/feedback.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Function: {function_type}\n")
            f.write(f"Query: {query}\n")
            f.write(f"Response: {response[:200]}...\n")
            f.write(f"Helpful: {helpful}\n")
    except Exception as e:
        print(f"Error saving feedback: {e}")

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    function_type = data.get("function")
    user_input = data.get("input", "").strip()
    
    if not user_input:
        return jsonify({"error": "Please provide input"}), 400

    try:
        if function_type == "question":
            response = answer_question(user_input)
        elif function_type == "summarize":
            response = summarize_text(user_input)
        elif function_type == "creative":
            response = generate_creative_content(user_input)
        else:
            return jsonify({"error": "Invalid function type"}), 400
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json
    save_feedback(
        data.get("function"),
        data.get("query"),
        data.get("response"),
        data.get("helpful")
    )
    return jsonify({"message": "Thank you for your feedback!"})

# ----------------------------
# Startup
# ----------------------------
if __name__ == "__main__":
    if GEMINI_API_KEY is None:
        raise RuntimeError("API key not configured. Set GOOGLE_API_KEY in .env")
    print("✅ Gemini API key configured.")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
