import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import pinecone
from langchain.vectorstores import Pinecone

app = Flask(__name__)
CORS(app, origins=["*"])  # Replace with your frontend domain or URL

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__ec5f7d678abe4b0f9a71f0311be34540"
os.environ["LANGCHAIN_PROJECT"] = "Nyay-API"


@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the input sentence from the JSON request
        data = request.get_json()
        if 'sentence' not in data:
            return jsonify({'error': 'Input sentence not provided'}), 400

        # Append "Fuck you" to the input sentence
        input_sentence = data['sentence']
        output_sentence = f"{input_sentence} Fuck you"

        return jsonify({'result': output_sentence})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
