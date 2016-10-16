import os
import urllib2
import json

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from goose import Goose


g = Goose()
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

keyword_dictionary = []

with open('keywords.txt', 'r') as data_file:
    for line in data_file:
        keyword_dictionary.append(line.rstrip())
print keyword_dictionary

class Data(db.Model):
    __tablename__ = 'news_articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String)
    title = db.Column(db.String)
    text = db.Column(db.String)
    relevancy = db.Column(db.String, default="0")
    cluster = db.Column(db.String)
    feedback_relevancy = db.Column(db.String)
    feedback_cluster = db.Column(db.String)
    keywords = db.Column(db.String)

    def __init__(self, url=None, text=None, title = None, relevancy=None, cluster=None, feedback_relevancy=None, feedback_cluster=None, keywords=None):
        self.url = url
        self.title = title
        self.text = text
        self.relevancy = float(relevancy)
        self.cluster = cluster
        self.feedback_relevancy = feedback_relevancy
        self.feedback_cluster = feedback_cluster
        self.keywords = keywords

    def to_dict(self):
        data_dict = {
        "id": self.id,
        "url" :self.url,
        "title" : self.title,
        "text": self.text,
        "relevancy": self.relevancy,
        "cluster":self.cluster ,
        "feedback_relevancy" :self.feedback_relevancy,
        "feedback_cluster": self.feedback_cluster,
        "keywords": self.keywords


        }
        return data_dict


@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

class HTMLArticle(Resource):
    def post(self):
        new_article = request.get_json(force=True)
        article = g.extract(raw_html=new_article['html'])
        disable_text = new_article.get('disable_text')
        title = article.title
        text = article.cleaned_text
        is_relevant = 0
        keywords = ["MSF", "Doctors Without Borders", "abduct", "kidnap", "kill"]

        input_data = Data(url=None, text=text, title=title, relevancy = is_relevant, keywords=keywords)
        db.session.add(input_data)
        db.session.commit()
        if disable_text == '1':
            text = None
        data = {'id': input_data.id, 'title': title, 'text': text, 'relevancy': is_relevant, 'keywords': keywords}
        return jsonify(data)


class Article(Resource):
    def post(self):
        new_article = request.get_json(force=False)
        try:
            new_entry = Data(**new_article)
            db.session.add(new_entry)
            db.session.commit()
        except Exception, e:
            return(jsonify({"success": False}))
        return jsonify({"success":True, "data":new_entry.to_dict()})

    def get(self):
        url = request.args.get('url')
        disable_text = request.args.get('disable_text')
        print(url)
        article = g.extract(url=url)
        title = article.title
        text = article.cleaned_text
        is_relevant = 0
        keywords = {}
        try:
            input_data = Data.query.filter_by(url=url).first()
            is_relevant = input_data.relevancy
            keywords = input_data.keywords
        except:
            print('in get')
            for k in keyword_dictionary:
                if k in text:
                    if k in keywords:
                        keywords[k]+=1
                    else:
                        keywords[k]=1
            input_data = Data(url=url, text=text, title=title, relevancy = is_relevant, keywords=str(keywords))
            db.session.add(input_data)
            db.session.commit()
        if disable_text == '1':
            text = None
        data = {'id': input_data.id, 'title': title, 'text': text, 'relevancy': "{0:.2f}".format(float(is_relevant)), 'keywords': keywords}
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
            if float(latest_news.relevancy) <1 and feedback_info == "1":
                latest_news.relevancy = float(latest_news.relevancy) + 0.1
                data = latest_news.relevancy
                db.session.commit()
            if float(latest_news.relevancy) >0 and feedback_info == '0':
                latest_news.relevancy = float(latest_news.relevancy) - 0.1
                data = latest_news.relevancy
                db.session.commit()
            latest_news.feedback_relevancy = feedback_info
            db.session.commit()
            return jsonify({'success': True, 'relevancy': "{0:.2f}".format(float(latest_news.relevancy))})
        except Exception, e:
            return jsonify({'success': False, 'data': e})
        return jsonify({'success': True, 'relevancy': data})

class DataDetails(Resource):
    def get(self, data_id):
        try:
            d = Data.query.filter_by(id=int(data_id)).first()
            data = d.to_dict()
        except Exception, e:
            return jsonify({'success': False})
        return jsonify({'success': True, 'data': data})

    def delete(self, data_id):
        data = Data.query.filter_by(id=int(data_id)).first()
        db.session.delete(data)
        db.session.commit()

class ListData(Resource):
    def get(self):
        data = Data.query.all()
        all_reports = []
        for r in data:
            all_reports.append(r.to_dict())
        return jsonify({'data': all_reports})


api.add_resource(Article, '/article')
api.add_resource(Feedback, '/feedback')
api.add_resource(DataDetails, '/data/<data_id>')
api.add_resource(ListData, '/list')
api.add_resource(HTMLArticle, '/html_article')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
