# Personal AI Assistant

A locally-running AI assistant that learns and improves from interactions. This assistant uses a local language model and maintains a history of conversations to provide more contextually relevant responses over time.

## Features

- 🤖 Local Language Model (OPT-350M)
- 📚 Conversation History & Learning
- 🔍 Context-Aware Responses
- 💡 Self-Improvement Through Feedback
- 🎯 Relevant Document Retrieval
- 🌐 Modern Web Interface

## Technical Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Language Model**: OPT-350M (via Hugging Face Transformers)
- **Embeddings**: Sentence Transformers
- **Vector Storage**: FAISS
- **UI Components**: Font Awesome, Google Fonts

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd personal-ai-assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python src/main.py
```

5. Open your web browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
personal-ai-assistant/
├── src/
│   ├── main.py              # Flask application entry point
│   ├── langchain/
│   │   ├── llm.py          # Language model implementation
│   │   └── retriever.py    # Document retrieval and storage
│   └── ui/
│       ├── index.html      # Web interface
│       └── script.js       # Frontend functionality
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## How It Works

1. **User Input**: Users can interact with the assistant through a modern web interface.
2. **Context Retrieval**: The system searches through previous interactions to find relevant context.
3. **Response Generation**: The local language model generates responses based on the user's input and retrieved context.
4. **Learning**: Each interaction is stored and indexed for future reference.
5. **Feedback Loop**: The system can incorporate user feedback to improve future responses.

## Features in Detail

### Local Language Model
- Uses the OPT-350M model for generating responses
- Runs completely locally, ensuring privacy
- Configurable generation parameters

### Context-Aware Responses
- Maintains a history of all interactions
- Uses FAISS for efficient similarity search
- Retrieves relevant past conversations

### Modern Interface
- Clean, responsive design with Tailwind CSS
- Real-time updates
- Conversation history view
- Feedback mechanism

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
