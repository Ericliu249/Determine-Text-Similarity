from flask import Flask, request, jsonify
import markdown
import os
from .similarity import Similarity

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
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
    text_list = request_data['text_list']
    similarity = Similarity().get_result(text_list)
    return jsonify({
        'message': "Computed the similarity between two texts successfully",
        'similarity': similarity
    })