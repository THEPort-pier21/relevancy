from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/')
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
    port = int(os.eniron.get("PORT", 5000))
    app.run(debug=True)
