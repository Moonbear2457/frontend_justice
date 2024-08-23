from flask import Flask, request, render_template, jsonify

# Mocked DBManager and generate_embedding_pure for testing purposes
class DBManager:
    def get_all_summary_vectors(self):
        # Normally, this would fetch summary vectors from the database.
        return []
    
    def get_all_sachverhalt_vectors(self):
        # Normally, this would fetch sachverhalt vectors from the database.
        return []
    
    def get_all_entscheid_vectors(self):
        # Normally, this would fetch entscheid vectors from the database.
        return []
    
    def get_all_grundlagen_vectors(self):
        # Normally, this would fetch grundlagen vectors from the database.
        return []
    
    def find_similar_vectors(self, target_vector, vectors, top_n):
        # Normally, this would find the most similar vectors from the provided data.
        # For testing, we return a mock list of similar vectors.
        return [
            (1, "parsed_id_1", 0.95),
            (2, "parsed_id_2", 0.92)
        ]
    
    def get_texts_from_vectors(self, vectors):
        # Normally, this would fetch text data based on the vectors from the database.
        # For testing, we return mock text data.
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
    # Normally, this would generate an embedding vector using OpenAI's API.
    # For testing, we return a mock vector.
    return [0.1, 0.2, 0.3]

def find_similar_documents(target_vector, db, top_n):
    """Mock function to return similar documents for testing."""
    # Normally, this would involve complex logic to find similar documents.
    # Here, we return a mock list of documents.
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
    
    db = DBManager()
    target_vector = generate_embedding_pure(user_input)  # Generate a mock embedding vector

    if target_vector is None:
        return jsonify("Failed to generate a meaningful response.")
    
    top_n = 5
    similar_documents = find_similar_documents(target_vector, db, top_n)

    if similar_documents:
        response = similar_documents[0]["text"]  # Return the top result
    else:
        response = "I couldn't find any relevant information."

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
