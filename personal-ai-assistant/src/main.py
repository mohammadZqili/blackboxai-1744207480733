from flask import Flask, request, jsonify, render_template
from langchain.llm import LLM
from langchain.retriever import Retriever
import os

app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'ui'),
            template_folder=os.path.join(os.path.dirname(__file__), 'ui'))

# Initialize LLM and Retriever
llm = LLM()
retriever = Retriever()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input = data.get('input')
    
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    try:
        # Retrieve relevant context
        context = retriever.retrieve(user_input)
        
        # Generate response
        response = llm.generate(user_input, context)
        
        # Store the interaction
        retriever.add_interaction(user_input, response)
        
        return jsonify({
            'response': response,
            'context': context
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    interaction_id = data.get('interaction_id')
    feedback = data.get('feedback')
    
    try:
        # Update the interaction with feedback
        retriever.add_feedback(interaction_id, feedback)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    try:
        history = retriever.get_interaction_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
