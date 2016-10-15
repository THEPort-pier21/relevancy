import os
import urllib2

from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from goose import Goose

g = Goose()

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

    def get(self):
        url = request.args.get('url')
        print(url)
        article = g.extract(url=url)
        title = article.title
        text = article.cleaned_text
        is_relevant = False

        data = {'title': title, 'text': text, 'relevancy': is_relevant}
        return jsonify(data)

api.add_resource(Article, '/article')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
