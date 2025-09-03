import os
import uuid
from flask import Blueprint, jsonify, request, current_app
from app.langchain.invoke_langchain import create_prompt_template, invoke_langchain
from app.main.utils.core import extract_text_from_pdf, split_text_into_chunks


doc_blueprint = Blueprint("document", __name__)


@doc_blueprint.route("/upload/doc", methods=["POST"])
def uploadFile():

    if "file" not in request.files:
        return jsonify({"error": "document not found"}), 400

    file = request.files["file"]
    current_directory = os.getcwd()

    # Create the tmp directory if it doesn't exist
    new_directory = os.path.join(current_directory, "tmp")
    os.makedirs(new_directory, exist_ok=True)

    filename = os.path.basename(file.filename).strip()

    if not filename:
        return jsonify({"error": "Invalid file name"}), 400

    file_path = os.path.join(new_directory, filename)

    file.save(file_path)

    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        extracted_text = extract_text_from_pdf(file_path)
    elif ext == "txt":
         with open(file_path, "r", encoding="utf-8") as f:
            extracted_text = f.read()
    
    chunks = split_text_into_chunks(extracted_text)

    for chunk in chunks:
        embedding = current_app.embedding_service.generate_embeddings(chunk)
        doc_id = str(uuid.uuid4())
        metadata = {"file_name": file.filename}

        current_app.vectorstore.add_document(
            doc_id=doc_id,
            text=chunk,
            embedding=embedding,
            metadata=metadata
        )

    return jsonify({"message": "Document uploaded successfully", "chunks": chunks}), 200


@doc_blueprint.route('/query', methods=['POST'])
def query_rag():
    """
    Perform a full RAG workflow:
    1. Get user query
    2. Retrieve relevant chunks from ChromaDB
    3. Generate answer using GPT
    """
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    # 1. Generate query embedding
    query_embedding = current_app.embedding_service.generate_embeddings(question)

    # 2. Search in ChromaDB for relevant chunks
    search_results = current_app.vectorstore.query(query_embedding, top_k=3)

    retrieved_chunks = search_results["documents"][0]

    if not retrieved_chunks:
        return jsonify({"answer": "No relevant documents found."}), 200

    # 3. Build prompt for GPT
    context_text = "\n\n".join(retrieved_chunks)
    prompt = (
        "You are a helpful assistant. "
        "Use the following context to answer the question. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer:"
    )
    data = {"context_text": context_text, "question": question}
    prompt_template = create_prompt_template(prompt)

    response = invoke_langchain(prompt_template, data)

    print(response,"ayushman you are here.")

    answer = response.content

    # 5. Return the result
    return jsonify({
        "question": question,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    })
