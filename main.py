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

@app.route('/', methods=['POST'])
def home():
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part received in the request"}), 400

    uploaded_file = request.files['file']

    # if uploaded_file.filename == '':
    #     return jsonify({"error": "No selected file"}), 400

    # if allowed_file(uploaded_file.filename):
    #     filename = os.path.join(app.config['UPLOAD_FOLDER'], str(uploaded_file.filename))
    #     uploaded_file.save(filename)

    #     df = None

    #     if filename.endswith('.csv'):
    #         df = pd.read_csv(filename)
    #     else:
    #         df = pd.read_excel(filename)

    #     llm = ChatOpenAI(
    #             model="gpt-3.5-turbo-0613"
    #     )
    #     print("Creating agent...")
    #     agents[ip_address] = create_pandas_dataframe_agent(
    #         llm,
    #         df,
    #         verbose=True,
    #         agent_type=AgentType.OPENAI_FUNCTIONS,
    #         agent_executor_kwargs={"handle_parsing_errors": True},
    #     )
    #     print("file uploaded successfully")
    #     return jsonify({"message": "File uploaded successfully", "ip_address": ip_address}), 200
    # else:
    #     return jsonify({"error": "Invalid file format"}), 400

@app.route('/chat', methods=['POST'])
def chat_with_agent():
    try:
        user_input = request.form.get('user_input')

        if not user_input:
            return jsonify({"error": "Invalid or missing 'user_input' in the request"}), 400

        # Append "Fuck you" to the input query
        output_query = f"{user_input} Fuck you"

        return jsonify({'result': output_query})

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
