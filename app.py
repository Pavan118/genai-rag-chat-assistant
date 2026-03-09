from flask import Flask, request, jsonify, render_template
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

print("Starting server...")

# Load documents
with open("docs.json") as f:
    documents = json.load(f)

print("Documents loaded")

# Store embeddings
embeddings = []
texts = []

# Fake embedding generator (for testing)
def generate_embedding(text):
    return np.random.rand(384)

print("Generating embeddings...")

for doc in documents:
    emb = generate_embedding(doc["content"])
    embeddings.append(emb)
    texts.append(doc["content"])

embeddings = np.array(embeddings)

print("Embeddings ready")

# Retrieve relevant context
def retrieve_context(query):

    query = query.lower()

    for doc in documents:
        if "password" in query and "password" in doc["content"].lower():
            return doc["content"]

        if "account" in query and "create" in doc["content"].lower():
            return doc["content"]

        if "upload" in query and "upload" in doc["content"].lower():
            return doc["content"]

        if "profile" in query and "profile" in doc["content"].lower():
            return doc["content"]

        if "delete" in query and "delete" in doc["content"].lower():
            return doc["content"]

    return "Sorry, I couldn't find information related to your question."

# Fake LLM response
def ask_llm(context, question):

    # Simply return the most relevant document sentence
    lines = context.split("\n")

    if len(lines) > 0:
        return lines[0]

    return "Sorry, I could not find an answer in the documents."

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json
    message = data["message"]

    context = retrieve_context(message)

    answer = ask_llm(context, message)

    return jsonify({
        "reply": answer,
        "retrievedChunks": 3
    })



import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)