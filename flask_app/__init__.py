from flask import Flask, request, jsonify
import markdown
import os
from datetime import datetime
from .similarity import Similarity

app = Flask(__name__)

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/Data Challenge.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)

@app.route("/similarity", methods=['POST'])
def check_similarity():
    """Present some documentation"""
    request_data = request.get_json()
    stopwords = request.args.get('stopwords', True)
    text_a = request_data['text_a']
    text_b = request_data['text_b']
    if stopwords == 'false' or stopwords == 'False':
        similarity = Similarity(False).get_result(text_a, text_b)
    else:
        similarity = Similarity(True).get_result(text_a, text_b)
    return jsonify({
        'message': "Computed the similarity between two texts successfully",
        'similarity': similarity
    })