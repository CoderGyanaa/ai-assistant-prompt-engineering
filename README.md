# 🤖 AI Assistant - Prompt Engineering Project

A powerful web-based AI Assistant built with Flask and Google's Gemini 2.5 Flash API, demonstrating advanced prompt engineering techniques and natural language processing capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Prompt Engineering](#prompt-engineering)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

This AI Assistant is a **Prompt Engineering project** that showcases how different prompt styles can dramatically affect AI responses. Built as part of a comprehensive study on AI interaction design, this application demonstrates:

- **Multiple prompt strategies** for the same task
- **Real-time AI responses** using Google's Gemini API
- **User feedback collection** for continuous improvement
- **Clean, intuitive interface** for seamless interaction

## ✨ Features

### Core Functions

1. **📚 Question Answering**
   - Provides comprehensive, detailed answers to factual questions
   - Uses context-rich prompts for better responses
   - Supports multiple answer styles (direct, detailed, simple)

2. **📝 Text Summarization**
   - Condenses long articles into concise summaries
   - Offers bullet-point and paragraph formats
   - Maintains key information while reducing length

3. **✨ Creative Content Generation**
   - Generates stories, poems, and creative ideas
   - Adapts style based on user request
   - Produces engaging, original content

### Additional Features

- ✅ Real-time AI-powered responses
- ✅ User feedback collection system
- ✅ Rate limit handling
- ✅ Multiple prompt engineering strategies
- ✅ Responsive web interface
- ✅ Automatic model selection
- ✅ Error handling and recovery

## 🎥 Demo

[Add screenshots or GIF demo here]

**Live Demo:** (https://ai-assistant-17eb.onrender.com/)

## 🛠 Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0.0** - Web framework
- **Google Generative AI** - Gemini 2.5 Flash API

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern gradients and animations
- **JavaScript (Vanilla)** - Interactivity and API calls

### AI Model
- **Gemini 2.5 Flash** - Google's advanced language model
- Fast response times with generous free tier limits

## 📁 Project Structure

```
ai-assistant/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
│
├── templates/
│   └── index.html             # Main web interface
│
├── static/
│   └── style.css              # CSS styling
│
├── feedback/
│   └── feedback.txt           # User feedback storage (auto-generated)
│
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-assistant.git
cd ai-assistant
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Configuration

### Get Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Set Up Environment Variables

**Option 1: Create .env file (Recommended)**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**Option 2: Environment Variable**

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY='your_api_key_here'
```

**Option 3: Direct in app.py**

Edit line 9 in `app.py`:
```python
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'your_api_key_here')
```

## 💻 Usage

### Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the AI Assistant

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Select a function:**
   - Answer Questions
   - Summarize Text
   - Generate Creative Content

3. **Enter your prompt** in the text area

4. **Click "Generate Response"** and wait for the AI

5. **Provide feedback** using the thumbs up/down buttons

### Example Prompts

**Questions:**
```
What is machine learning?
Explain quantum computing
How does photosynthesis work?
```

**Summarization:**
```
[Paste any long article or document]
```

**Creative Content:**
```
Write a story about a robot learning emotions
Create a poem about technology
Generate 5 app ideas for students
```

## 🎯 Prompt Engineering

This project demonstrates **three distinct prompt engineering strategies** for each function:

### 1. Question Answering Prompts

```python
'direct': "Answer this question directly and concisely in 2-3 sentences: {question}"
'detailed': "Provide a comprehensive and detailed answer with context and examples for: {question}"
'simple': "Explain this in simple, easy-to-understand terms suitable for a beginner: {question}"
```

### 2. Summarization Prompts

```python
'brief': "Provide a brief summary in 2-3 sentences of the following text:\n\n{text}"
'detailed': "Summarize the main points and key details of this text in a structured way:\n\n{text}"
'bullet': "Create a bullet-point summary highlighting the key points of this text:\n\n{text}"
```

### 3. Creative Content Prompts

```python
'story': "Write a creative and engaging short story (200-300 words) about: {prompt_text}"
'poem': "Create a beautiful and expressive poem about: {prompt_text}"
'idea': "Generate 3-5 innovative and creative ideas related to: {prompt_text}"
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/process` | POST | Process AI requests |
| `/feedback` | POST | Submit user feedback |
| `/test-api` | GET | Test API connection |
| `/list-models` | GET | List available Gemini models |

### Example API Usage

```javascript
// Process a question
fetch('/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        function: 'question',
        input: 'What is AI?'
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```


## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions

- Add more AI functions (translation, code generation, etc.)
- Implement user authentication
- Add response history/session management
- Create unit tests
- Improve UI/UX design
- Add more prompt engineering examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini API** for providing powerful AI capabilities
- **Flask** for the excellent web framework
- **Prompt Engineering Course** for inspiration and techniques
- All contributors and testers

## 📞 Contact

**Your Name** - Gyana Ranjan Sahoo

Project Link: https://github.com/CoderGyanaa/ai-assistant-prompt-engineering
---

## 📊 Project Stats

- **Lines of Code:** ~500+
- **Functions:** 3 core AI functions
- **Prompt Variations:** 9+ different prompts
- **API Integration:** Google Gemini 2.5 Flash
- **Supported Models:** 40+ Gemini models

## 🎓 Academic Context

This project was developed as part of a **Prompt Engineering course** to demonstrate:
- Understanding of prompt design principles
- Practical AI integration skills
- User experience considerations
- Feedback-driven improvement methodology

---

**Made with ❤️ and ☕ by Gyana**

*Star ⭐ this repository if you find it helpful!*
