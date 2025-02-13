from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)


# Configure Swagger
swagger = Swagger(app)

# In-memory storage for documents
documents = {}
item_id_counter = 1


@app.route('/documents', methods=['GET'])
def list_documents():
    """
    List all documents.
    ---
    tags:
      - Documents
    parameters:
      - name: author
        in: query
        description: The author of the document.
        required: false
        schema:
          type: string
      - name: tags
        in: query
        description: The tags of the document.
        required: false
        schema:
          type: string
    responses:
      200:
        description: .
        content:
          application/json:
            schema:
              type: array
              documents:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique ID of the document.
                  title:
                    type: string
                    description: The title of the document.
                  author:
                    type: string
                    description: The author of the document.
                  tags:
                    type: string
                    description: The list of tags for categorizing the document.
    """
    filtered_documents = []
    author = request.args.get('author')
    tags = request.args.get('tags')
    for document in documents.values():
        if ((document['author'].lower() == (author.lower() if author else document['author'].lower())) and ((tags.lower() in document['tags'].lower()) if tags else True)):
            filtered_document = document.copy()
            filtered_document.pop("content", None)
            filtered_documents.append(filtered_document)   
    return jsonify({'success': True, 'message': f'{filtered_documents}'}),200    

@app.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """
    Content of the Document.
    ---
    tags:
      - Documents
    parameters:
      - in: path
        name: document_id
        required: true
        description: The ID of the document to update.
        schema:
          type: integer
    responses:
      200:
        description: .
        content:
          application/json:
            schema:
              type: array
              documents:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique ID of the document.
                  title:
                    type: string
                    description: The title of the document.
                  content:
                    type: string
                    description: The content for the document.  
                  author:
                    type: string
                    description: The author of the document.
                  tags:
                    type: string
                    description: The list of tags for categorizing the document.
      404:
        description: Bad Input - Document not found.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
    """
    document = documents.get(int(document_id))
    if not document:
        return jsonify({"success": False, "message": "Document not found."}), 404
    return jsonify({"success": True, "message": document.get("content")}), 200
   
@app.route('/documents/<document_id>', methods=['PUT'])
def update_document(document_id):
    """
    Update the completion status of an item.
    ---
    tags:
      - Documents
    parameters:
      - in: path
        name: document_id
        required: true
        description: The ID of the document to update.
        schema:
          type: integer
      - in: body
        name: body
        required: true
        description: JSON object containing the new content for document.
        schema:
          type: object
          properties:
            content:
              type: string
              description: The new content for document.
              example: true
              required: true
    responses:
      200:
        description: Document successfully updated.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
      404:
        description: Document not found.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
    """
    global documents
    document = None
    data = request.get_json()
    
    if not data or "content" not in data:
        return jsonify({"success": False, "message": "Invalid input. 'content' field is required."}), 400
    
    document = documents.get(int(document_id))

    if document is None:
        return jsonify({"success": False, "message": f"Document with ID {document_id} not found."}), 404

    document["content"] = data["content"]
    return jsonify({"success": True, "message": f"Document with ID {document_id} content updated to new content."}), 200


@app.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """
    Delete an document from the Documents by its ID.
    ---
    tags:
      - Documents
    parameters:
      - in: path
        name: document_id
        required: true
        description: The ID of the item to delete.
        schema:
          type: integer
    responses:
      200:
        description: Document successfully deleted.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
      404:
        description: Document not found.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
    """
    global documents
    for document in documents.values():
        if document["id"] == int(document_id):
            document = document
            break

    if document is None:
        return jsonify({"success": False, "message": f"Document with ID {document_id} not found."}), 404

    del documents[int(document_id)]
    return jsonify({"success": True, "message": f"Document with ID {document_id} has been successfully deleted."}), 200


@app.route("/documents", methods=["POST"])
def add_document():
    """
    Add a new item to the list.
    ---
    tags:
      - Documents
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: JSON object containing the description and completion status of the item.
        schema:
          type: object
          properties:
            title:
              type: string
              description: The title of the document.
              required: true
            content:
              type: string
              description: The content for the document.
              required: true
            author:
              type: string
              description: The author of the document.
              required: true
            tags:
              type: string
              description: The list of tags for categorizing the document.
              required: true
    responses:
      201:
        description: Document successfully added.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
      400:
        description: Bad Request - Invalid input.
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                message:
                  type: string
    """
    global item_id_counter
    data = request.get_json()

    if not data or "content" not in data or not data["content"].strip() or "author" not in data or "title" not in data or "tags" not in data: 
        return jsonify({"success": False, "message": "All fields are required."}), 400

    document = {
        "id": item_id_counter,
        "title": data["title"],
        "content": data["content"],
        "author": data["author"],
        "tags": data["tags"]
    }
    documents[item_id_counter] = document
    item_id_counter += 1

    return jsonify({"success": True, "message": f"Document added: {data['title']}"}), 201


if __name__ == "__main__":
    app.run(debug=True)