from flask import Flask, request, jsonify
from flask_cors import CORS
import markdown
import os
from .similarity import Similarity

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

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
        'success': True,
        'message': "Computed the similarity between two texts successfully",
        'similarity': similarity
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405