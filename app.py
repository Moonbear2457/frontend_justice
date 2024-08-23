from flask import Flask, request, render_template, jsonify
from db import DBManager
from embed import generate_embedding_pure

app = Flask(__name__)

def combine_and_rank_vectors(similar_summaries_vector_list, similar_sachverhalte_vector_list, 
                             similar_entscheide_vector_list, similar_grundlagen_vector_list, top_n):
    """Combine and rank the top N results from different vector lists."""
    
    combined_vectors = []

    for vector in similar_summaries_vector_list:
        combined_vectors.append((vector, "Summary"))

    for vector in similar_sachverhalte_vector_list:
        combined_vectors.append((vector, "Sachverhalt"))

    for vector in similar_entscheide_vector_list:
        combined_vectors.append((vector, "Entscheide"))

    for vector in similar_grundlagen_vector_list:
        combined_vectors.append((vector, "Grundlagen"))

    combined_vectors.sort(key=lambda x: x[0][2], reverse=True)

    top_vectors = combined_vectors[:top_n]

    return top_vectors

def find_similar_documents(target_vector, db, top_n):
    """Find similar documents based on user input."""
    
    summary_vectors = db.get_all_summary_vectors()
    sachverhalt_vectors = db.get_all_sachverhalt_vectors()
    entscheid_vectors = db.get_all_entscheid_vectors()
    grundlagen_vectors = db.get_all_grundlagen_vectors()
    
    similar_summaries_vector_list = db.find_similar_vectors(target_vector, summary_vectors, top_n)
    similar_sachverhalte_vector_list = db.find_similar_vectors(target_vector, sachverhalt_vectors, top_n)
    similar_entscheide_vector_list = db.find_similar_vectors(target_vector, entscheid_vectors, top_n)
    similar_grundlagen_vector_list = db.find_similar_vectors(target_vector, grundlagen_vectors, top_n)
    
    top_combined_vectors = combine_and_rank_vectors(similar_summaries_vector_list, 
                                                    similar_sachverhalte_vector_list, 
                                                    similar_entscheide_vector_list, 
                                                    similar_grundlagen_vector_list, top_n)
    
    results = []
    for vector, origin in top_combined_vectors:
        id, parsed_id, similarity = vector
        text_info = db.get_texts_from_vectors([(id, parsed_id, vector)])
        if text_info:
            text = text_info[0]
            results.append({
                "origin": origin,
                "id": text['ID'],
                "parsed_id": text['parsed_id'],
                "similarity": f"{similarity:.4f}",
                "text": text['summary_text'],
                "sachverhalt": text['sachverhalt'],
                "entscheid": text['entscheid'],
                "grundlagen": text['grundlagen'],
                "forderung": text['forderung'],
                "file_path": text['file_path']
            })
    return results

def find_rechtsgrundlage(target_vector, db, top_n):
    articles_vectors = db.get_all_articles_vectors()
    similar_vectors = db.find_similar_aritcle_vectors(target_vector, articles_vectors, top_n)
    similar_articles = db.get_articles_from_vectors(similar_vectors)

    return similar_articles

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("Boiler Kopie.html")

@app.route("/get", methods=["GET"])
def chatbot_response():
    user_input = request.args.get('msg')
    if not user_input:
        return jsonify("Sorry, I didn't get that.")
    
    db = DBManager()
    target_vector = generate_embedding_pure(user_input)

    if target_vector is None:
        return jsonify("Failed to generate a meaningful response.")
    
    top_n = 5
    similar_documents =  find_similar_documents(target_vector, db, top_n)

    if similar_documents:
        response = similar_documents[0]["text"] # returns the top result
    else:
        response = "I couldn't find any relevant information."

    return jsonify(response)

if __name__=="__main__":
    app.run(debug=True)    