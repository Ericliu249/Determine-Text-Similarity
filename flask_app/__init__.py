from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import markdown
import os
from .similarity import Similarity

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    """Add headers to response
    """
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

@app.route("/")
def index():
    """Get the README.md
    """
    try:
        # Open the README file
        with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

            # Read the content of the file
            content = markdown_file.read()

            # Convert to HTML
            readme = markdown.markdown(content)
            return readme
    except:
        abort(422)


@app.route("/similarity", methods=['POST'])
def check_similarity():
    """Takes two texts and return the similarity between them
    """
    request_data = request.get_json()
    stopwords = request.args.get('stopwords', True)
    try:
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
    except:
        abort(422)

@app.errorhandler(404)
def not_found(error):
    """Returns an JSON error message if the requsted resource is not found
    """
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    """Returns an JSON error message if the requst is not processable
    """
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(400)
def bad_request(error):
    """Returns an JSON error message if a user made an inappropriate requst
    """
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def not_allowed(error):
    """Returns an JSON error message if the request method is not allowed
    """
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405