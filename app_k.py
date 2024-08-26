import openai
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

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

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("Boiler_k.html")

@app.route("/get", methods=["GET"])
def chatbot_response():
    user_input = request.args.get('msg')
    if not user_input:
        return jsonify("Sorry, I didn't get that.")
    

    try:
        # Make a call to the OpenAI API using the new interface
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly knowledgeable legal assistant specializing in Swiss law. "
                        "You should only provide information and answer questions related to Swiss law. "
                        "If a user asks about anything outside of this domain, politely decline to answer, "
                        "stating that your expertise is limited to Swiss legal matters."
                    ),
                },
                {"role": "user", "content": user_input},
            ]
        )

        # Extract the assistant's reply from the response
        gpt_response = response.choices[0].message.content
        print(gpt_response)

    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return jsonify(f"Sorry, an error occurred: {str(e)}")

    return jsonify(gpt_response)

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
