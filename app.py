from flask import Flask, request, render_template, jsonify
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure Gemini API


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)


# Try to use the best available model with good free tier limits
def get_model():
    """Get the best available Gemini model with generous free tier"""
    # Priority: Use models with best free tier limits
    # Gemini Flash models have 15 RPM and 1500 RPD free tier
    # Gemini Pro models have very limited free tier
    
    preferred_models = [
        'gemini-2.5-flash',              # Best balance - good free tier
        'gemini-flash-latest',           # Stable flash model
        'gemini-2.0-flash',              # Good free tier
        'gemini-2.0-flash-001',          # Stable version
        'gemini-2.5-flash-lite',         # Even more generous limits
        'gemini-flash-lite-latest',      # Lite version
    ]
    
    print("🔍 Looking for models with good free tier limits...")
    
    for model_name in preferred_models:
        try:
            model = genai.GenerativeModel(model_name)
            # Test if model works
            test_response = model.generate_content("Hi")
            print(f"✅ Using model: {model_name}")
            print(f"   This model has generous free tier limits!")
            return model
        except Exception as e:
            print(f"   Trying {model_name}... not available")
            continue
    
    # If preferred models don't work, list all and pick a flash model
    try:
        print("\n🔍 Checking all available models...")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name.replace('models/', '')
                # Prefer flash or lite models (better free tier)
                if 'flash' in model_name.lower() or 'lite' in model_name.lower():
                    try:
                        model = genai.GenerativeModel(model_name)
                        test_response = model.generate_content("Hi")
                        print(f"✅ Using model: {model_name}")
                        return model
                    except:
                        continue
    except Exception as e:
        print(f"⚠️ Error checking models: {str(e)}")
    
    # Last resort
    print("⚠️ Using fallback model")
    return genai.GenerativeModel('gemini-flash-latest')

# Initialize model
model = get_model()

# Ensure feedback directory exists
os.makedirs('feedback', exist_ok=True)

def answer_question(question):
    """Function to answer factual questions with different prompt styles"""
    prompts = {
        'direct': f"Answer this question directly and concisely in 2-3 sentences: {question}",
        'detailed': f"Provide a comprehensive and detailed answer with context and examples for: {question}",
        'simple': f"Explain this in simple, easy-to-understand terms suitable for a beginner: {question}"
    }
    
    try:
        # Use detailed prompt for better responses
        prompt = prompts['detailed']
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        if '429' in error_msg or 'quota' in error_msg.lower():
            return "⚠️ Rate limit reached! Please wait a moment and try again. The free tier has limits: 15 requests per minute, 1500 per day. Consider using shorter prompts or waiting 60 seconds."
        return f"Error generating response: {error_msg}"

def summarize_text(text):
    """Function to summarize text with different prompt approaches"""
    prompts = {
        'brief': f"Provide a brief summary in 2-3 sentences of the following text:\n\n{text}",
        'detailed': f"Summarize the main points and key details of this text in a structured way:\n\n{text}",
        'bullet': f"Create a bullet-point summary highlighting the key points of this text:\n\n{text}"
    }
    
    try:
        # Use bullet point format for better readability
        prompt = prompts['bullet']
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}. Please check your API key and try again."

def generate_creative_content(prompt_text):
    """Function to generate creative content with various styles"""
    
    # Detect the type of creative content requested
    if any(word in prompt_text.lower() for word in ['story', 'tale', 'narrative']):
        prompt = f"Write a creative and engaging short story (200-300 words) about: {prompt_text}"
    elif any(word in prompt_text.lower() for word in ['poem', 'poetry', 'verse']):
        prompt = f"Create a beautiful and expressive poem about: {prompt_text}"
    elif any(word in prompt_text.lower() for word in ['idea', 'concept', 'suggestion']):
        prompt = f"Generate 3-5 innovative and creative ideas related to: {prompt_text}"
    else:
        prompt = f"Create engaging creative content based on: {prompt_text}. Be imaginative and original."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating creative content: {str(e)}. Please check your API key and try again."

def save_feedback(function_type, query, response, helpful):
    """Save user feedback to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open('feedback/feedback.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Function: {function_type}\n")
            f.write(f"Query: {query}\n")
            f.write(f"Response: {response[:200]}...\n")
            f.write(f"Helpful: {helpful}\n")
    except Exception as e:
        print(f"Error saving feedback: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    function_type = data.get('function')
    user_input = data.get('input', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Please provide input'}), 400
    
    # Check if API key is configured
    if GEMINI_API_KEY == 'YOUR_API_KEY_HERE':
        return jsonify({'error': 'Please configure your GEMINI_API_KEY in the environment variables or app.py'}), 500
    
    # Process based on function type
    try:
        if function_type == 'question':
            response = answer_question(user_input)
        elif function_type == 'summarize':
            response = summarize_text(user_input)
        elif function_type == 'creative':
            response = generate_creative_content(user_input)
        else:
            return jsonify({'error': 'Invalid function type'}), 400
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    save_feedback(
        data.get('function'),
        data.get('query'),
        data.get('response'),
        data.get('helpful')
    )
    return jsonify({'message': 'Thank you for your feedback!'})

@app.route('/test-api', methods=['GET'])
def test_api():
    """Test endpoint to verify Gemini API connection"""
    try:
        if GEMINI_API_KEY == 'YOUR_API_KEY_HERE':
            return jsonify({
                'status': 'error',
                'message': 'API key not configured. Please set GEMINI_API_KEY.'
            })
        
        # Test with a simple prompt
        response = model.generate_content("Say 'API is working!' if you can read this.")
        return jsonify({
            'status': 'success',
            'message': 'Gemini API is configured correctly!',
            'response': response.text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'API test failed: {str(e)}'
        })

@app.route('/list-models', methods=['GET'])
def list_models():
    """List all available Gemini models for your API key"""
    try:
        models = genai.list_models()
        model_list = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                model_list.append({
                    'name': m.name,
                    'display_name': m.display_name,
                    'description': m.description
                })
        return jsonify({
            'status': 'success',
            'models': model_list
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error listing models: {str(e)}'
        })

if __name__ == '__main__':
    # Check API key on startup
    if GEMINI_API_KEY == 'YOUR_API_KEY_HERE':
        print("\n" + "="*60)
        print("⚠️  WARNING: GEMINI_API_KEY not configured!")
        print("="*60)
        print("Please set your Gemini API key:")
        print("1. Get your API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable: $env:GEMINI_API_KEY='your-api-key'")
        print("   OR edit app.py and replace 'YOUR_API_KEY_HERE' with your key")
        print("="*60 + "\n")
    else:
        print("✅ Gemini API key configured successfully!")
    
    app.run(host='0.0.0.0', port=5000)