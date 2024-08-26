import openai
import os
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from save_conversation import save_conversation_to_file, load_conversation_from_file

# Load Env variables from the .env file
load_dotenv()


# Set the API key
client = openai.Client(api_key = os.getenv("OPENAI_API_KEY"))

# Mocked DBManager and generate_embedding_pure for testing purposes
class DBManager:
    def get_all_summary_vectors(self):
        return []
    
    def get_all_sachverhalt_vectors(self):
        return []
    
    def get_all_entscheid_vectors(self):
        return []
    
    def get_all_grundlagen_vectors(self):
        return []
    
    def find_similar_vectors(self, target_vector, vectors, top_n):
        return [
            (1, "parsed_id_1", 0.95),
            (2, "parsed_id_2", 0.92)
        ]
    
    def get_texts_from_vectors(self, vectors):
        return [
            {
                "ID": 1,
                "parsed_id": "parsed_id_1",
                "summary_text": "This is a mock summary text.",
                "sachverhalt": "This is a mock Sachverhalt.",
                "entscheid": "This is a mock Entscheid.",
                "grundlagen": "These are mock Grundlagen.",
                "forderung": "This is a mock Forderung.",
                "file_path": "mock/path/to/file"
            }
        ]

def generate_embedding_pure(text):
    return [0.1, 0.2, 0.3]

def find_similar_documents(target_vector, db, top_n):
    return [
        {
            "origin": "Summary",
            "id": 1,
            "parsed_id": "parsed_id_1",
            "similarity": "0.9500",
            "text": "This is a mock summary text.",
            "sachverhalt": "This is a mock Sachverhalt.",
            "entscheid": "This is a mock Entscheid.",
            "grundlagen": "These are mock Grundlagen.",
            "forderung": "This is a mock Forderung.",
            "file_path": "mock/path/to/file"
        },
        {
            "origin": "Sachverhalt",
            "id": 2,
            "parsed_id": "parsed_id_2",
            "similarity": "0.9200",
            "text": "This is another mock summary text.",
            "sachverhalt": "This is another mock Sachverhalt.",
            "entscheid": "This is another mock Entscheid.",
            "grundlagen": "These are more mock Grundlagen.",
            "forderung": "This is another mock Forderung.",
            "file_path": "mock/path/to/another/file"
        }
    ]

app = Flask(__name__)

app.secret_key = os.getenv("SESSION_KEY")  # Set a secret key for session management, not used as of now.

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("Boiler_k.html")

@app.route("/get", methods=["GET"])
def chatbot_response():
    user_input = request.args.get('msg')
    if not user_input:
        return jsonify("Sorry, I didn't get that.")
    
    # Load existing conversation history from the file
    conversation = load_conversation_from_file()
    
    if not conversation:
        conversation = [
            {
                "role": "system",
                "content": (
                    "You are a highly knowledgeable legal assistant specializing in Swiss federal, cantonal, and communal law. "
                    "You should only provide information and answer questions related to Swiss federal, cantonal, or communal law. "
                ),
            }
        ]

    conversation.append({"role": "user", "content": user_input})

    if "test grundlagen" in user_input.lower():
        gpt_response = {
            "title": "Test Response",
            "summary": "This is a test summary.",
            "sachverhalt": "This is a test Sachverhalt.",
            "entscheid": "This is a test Entscheid.",
            "grundlagen": "This is a test of the Grundlagen section. It should appear on the right side.",
            "forderung": "This is a test Forderung."
        }
    else:
        try:
            # Make a call to the OpenAI API using the conversation history
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )

            gpt_response = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": gpt_response})
            save_conversation_to_file(conversation)
        
        except Exception as e:
            print(f"General error: {e}")
            return jsonify(f"Sorry, an unexpected error occurred: {str(e)}")

    return jsonify(gpt_response)

# Optional route to clear the conversation history
@app.route("/reset", methods=["GET"])
def reset_conversation():
    session.pop('conversation', None)
    return jsonify("Conversation history cleared.")


"""     db = DBManager()
    target_vector = generate_embedding_pure(user_input)  # Generate a mock embedding vector

    if target_vector is None:
        return jsonify("Failed to generate a meaningful response.")
    
    top_n = 5
    similar_documents = find_similar_documents(target_vector, db, top_n)

    if similar_documents:
        response = {
            "title": "Search Result",
            "summary": similar_documents[0]["text"],
            "sachverhalt": similar_documents[0]["sachverhalt"],
            "entscheid": similar_documents[0]["entscheid"],
            "grundlagen": similar_documents[0]["grundlagen"],
            "forderung": similar_documents[0]["forderung"]
        }
    else:
        response = "I couldn't find any relevant information." """


if __name__ == "__main__":
    app.run(debug=True)
    