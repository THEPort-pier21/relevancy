import os
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

class Article(Resource):
    def post(self):
        new_article = request.get_json(force=False)
        is_relevant = False
        data= {'relevancy': is_relevant, 'article': new_article}
        return jsonify(data)

api.add_resource(Article, '/article')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
