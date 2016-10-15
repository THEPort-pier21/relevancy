import os
import urllib2

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from goose import Goose


g = Goose()
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')


class Data(db.Model):
    __tablename__ = 'news_articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    text = db.Column(db.String)
    relevancy = db.Column(db.String)
    cluster = db.Column(db.String)
    feedback_relevancy = db.Column(db.String)
    feedback_cluster = db.Column(db.String)

    def __init__(self, url=None, text=None, title = None, relevancy=None, cluster=None, feedback_relevancy=None, feedback_cluster=None):
        self.url = url
        self.title = title
        self.text = text
        self.relevancy = relevancy
        self.cluster = cluster
        self.feedback_relevancy = feedback_relevancy
        self.feedback_cluster = feedback_cluster


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
        disable_text = request.args.get('disable_text')
        print(url)
        article = g.extract(url=url)
        title = article.title
        text = article.cleaned_text
        is_relevant = False

        input_data = Data(url=url, text=text, title=title, relevancy = is_relevant)
        db.session.add(input_data)
        db.session.commit()
        if disable_text == '1':
            text = None
        data = {'id': input_data.id, 'title': title, 'text': text, 'relevancy': is_relevant}
        return jsonify(data)

class Feedback(Resource):

    def get(self):
        #pass {feedback: 1 or 0, id: id of article}
        #user_feedback = request.get_json(force=False)
        feedback_id = request.args.get('id')
        feedback_info = request.args.get('feedback')
        data = feedback_info
        try:
            latest_news = Data.query.filter_by(id=int(feedback_id)).first()
            latest_news.feedback_relevancy = feedback_info
            db.session.commit()
        except Exception, e:
            return jsonify({'success': False, 'data': e})
        return jsonify({'success': True, 'data': data})

api.add_resource(Article, '/article')
api.add_resource(Feedback, '/feedback')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
