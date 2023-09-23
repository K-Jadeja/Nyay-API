import os
import detectlanguage
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone
from pinecone_utils import upsert_doc, retrieve_answer
from easygoogletranslate import EasyGoogleTranslate


app = Flask(__name__)
CORS(app, origins=["*"])  

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
# DETECT_LANGUAGE_API_KEY = os.environ.get("DETECT_LANGUAGE_API_KEY")
# detectlanguage.configuration.api_key = DETECT_LANGUAGE_API_KEY
detectlanguage.configuration.api_key = "2069169580e74f64a698f94d02cb7d38"
translator = EasyGoogleTranslate()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__ec5f7d678abe4b0f9a71f0311be34540"
os.environ["LANGCHAIN_PROJECT"] = "Nyay-API"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
@app.route('/', methods=['POST'])
def home():
    return "Hello World!"
@app.route('/uploads', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        if not os.path.exists('uploads'):
            os.makedirs('uploads')
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        try:
            upsert_doc()
            os.remove(file_path)
            return jsonify({"message": "Data uploaded successfully"}), 200
        except Exception as e:
            app.logger.error(f"An error occurred during upsert_doc: {str(e)}")
            return jsonify({"error": "An error occurred during data upload"}), 500

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form.get('user_input')

        if not user_input:
            return jsonify({"error": "Invalid or missing 'user_input' in the request"}), 400
        source_lang = detectlanguage.simple_detect(user_input)
        user_input = translator.translate(user_input, target_language='en')
        print("ahhh")
        output_query = retrieve_answer(user_input)
        print(output_query)
        result = translator.translate(output_query, target_language=source_lang)


        return jsonify({'result': result})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))

