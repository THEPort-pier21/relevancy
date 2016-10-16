import os
import urllib2
import json
import numpy
import math

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_restful import Resource, Api
from flask.ext.sqlalchemy import SQLAlchemy
from goose import Goose


vector = [9, 11, 10, 14, 7, 12, 16, 9, 1, 18, 5, 9, 10, 8, 18, 25, 6, 18, 11, 12, 55, 11, 16, 13, 11, 9, 13, 6, 18, 16, 13, 12, 11, 7, 23, 19, 6, 10, 6, 6, 7, 9, 11, 10, 10, 10, 35, 14, 5, 12, 13, 9, 19, 7, 11, 19, 14, 21, 9, 14, 8, 14, 13, 14, 12, 17, 21, 12, 16, 14, 14, 9, 10, 25, 7, 2, 8, 17, 11, 4, 19, 35, 7, 9, 19, 18, 10, 6, 16, 10, 6, 5, 29, 10, 15, 18, 10, 23, 8, 21, 9, 8, 7, 9, 10, 14, 16, 11, 17, 15, 4, 14, 9, 12, 16, 9, 17, 17, 11, 15, 6, 14, 15, 19, 15, 5, 23, 17, 10, 3, 6, 4, 12, 6, 18, 6, 9, 7, 8, 3, 4, 5, 12, 2, 2, 3, 3, 3, 3, 28, 6, 5, 11, 4, 5, 5, 9, 4, 3, 5, 8, 7, 7, 7, 3, 4, 1, 9, 5, 6, 10, 2, 5, 24, 2, 4, 29, 3, 13, 3, 3, 5, 21, 5, 4, 20, 5, 1, 3, 5, 7, 3, 5, 2, 2, 2, 4, 4, 2, 6, 2, 3, 2, 18, 3, 4, 14, 7, 2, 6, 7, 9, 4, 30, 6, 8, 4, 5, 8, 4, 5, 61, 26, 6, 3, 7, 5, 4, 4, 4, 2, 5, 1, 4, 7, 27, 4, 3, 10, 3, 5, 2, 1, 5, 6, 3, 6, 5, 4, 6, 7, 6, 8, 3, 0, 13, 3, 3, 19, 30, 2, 10, 6, 16, 4, 19, 7, 5, 12, 4, 5, 6, 22, 8, 11, 3, 8, 26, 6, 4, 5, 6, 4, 7, 8, 3, 17, 6, 5, 7, 11, 8, 9, 7, 4, 6, 7, 8, 5, 8, 12, 5, 2, 7, 1, 7, 1, 10, 4, 7, 4, 8, 6, 12, 10, 7, 25, 0, 8, 6, 7, 2, 12, 3, 5, 4, 5, 2, 15, 7, 6, 4, 32, 3, 10, 6, 13, 5, 19, 6, 7, 8, 6, 5, 16, 10, 7, 8, 8, 3, 8, 8, 6, 12, 1, 4, 7, 5, 3, 6, 4, 3, 2, 5, 2, 3, 4, 5, 22, 8, 5, 4, 5, 6, 8, 5, 7, 34, 10, 6, 7, 8, 8, 3, 7, 8, 6, 9, 6, 3, 12, 5, 12, 7, 5, 0, 9, 6, 4, 4, 10, 6, 10, 7, 5, 1, 5, 7, 3, 3, 8, 5, 7, 6, 7, 7, 2, 15, 4, 6, 9, 6, 6, 1, 6, 6, 5, 5, 3, 6, 10, 4, 8, 5, 6, 8, 5, 2, 51, 6, 16, 27, 5, 9, 5, 6, 2, 5, 4, 5, 4, 7, 1, 3, 3, 7, 6, 6, 5, 6, 6, 9, 3, 1, 15, 9, 6, 8, 3, 9, 7, 26, 6, 5, 2, 6, 6, 3, 4, 5, 3, 5, 6, 9, 5, 19, 3, 2, 7, 5, 4, 5, 10, 60, 5, 9, 4, 1, 8, 4, 3, 4, 18, 16, 9, 0, 9, 7, 6, 10, 5, 8, 4, 5, 5, 8, 8, 11, 14, 2, 7, 7, 5, 4, 3, 8, 4, 4, 5, 24, 7, 9, 6, 2, 9, 3, 25, 17, 6, 5, 5, 13, 6, 5, 3, 3, 4, 5, 4, 9, 15, 6, 5, 3, 5, 11, 8, 15, 7, 6, 9, 1, 3, 6, 3, 10, 4, 3, 5, 9, 13, 13, 5, 3, 9, 3, 7, 8, 10, 6, 2, 13, 6, 5, 5, 7, 6, 6, 7, 3, 7, 8, 30, 9, 4, 3, 6, 38, 60, 2, 17, 4, 7, 9, 8, 3, 5, 3, 7, 7, 3, 11, 7, 5, 6, 3, 3, 9, 9, 8, 5, 19, 7, 5, 5, 2, 9, 2, 3, 9, 5, 4, 3, 7, 11, 5, 9, 4, 5, 7, 7, 4, 6, 6, 7, 5, 7, 7, 4, 2, 5, 5, 4, 12, 9, 5, 26, 3, 6, 2, 6, 5, 8, 4, 10, 7, 13, 9, 7, 3, 4, 9, 5, 5, 4, 7, 6, 4, 17, 30, 3, 4, 6, 4, 2, 4, 15, 4, 8, 6, 17, 8, 14, 2, 8, 8, 7, 7, 2, 9, 0, 10, 4, 7, 3, 5, 4, 8, 7, 7, 6, 9, 24, 5, 5, 6, 4, 5, 14, 2, 6, 4, 2, 4, 13, 3, 5, 17, 5, 17, 4, 9, 8, 1, 6, 6, 5, 5, 5, 19, 3, 2, 6, 5, 26, 6, 6, 8, 3, 7, 11, 5, 11, 5, 12, 8, 6, 6, 3, 5, 5, 5, 8, 5, 25, 6, 1, 5, 4, 22, 6, 4, 1, 3, 4, 7, 7, 2, 12, 7, 5, 32, 5, 10, 5, 20, 5, 4, 8, 4, 6, 4, 8, 14, 26, 5, 3, 23, 16, 8, 7, 6, 7, 6, 6, 2, 10, 2, 3, 3, 4, 15, 14, 5, 12, 6, 2, 7, 15, 5, 6, 4, 7, 4, 3, 3, 5, 8, 8, 12, 5, 3, 9, 4, 43, 2, 4, 7, 3, 4, 8, 9, 6, 5, 5, 3, 8, 5, 9, 6, 5, 7, 2, 15, 5, 9, 2, 3, 6, 7, 20, 2, 11, 6, 3, 8, 14, 3, 8, 2, 4, 8, 9, 9, 18, 5, 7, 2, 9, 21, 7, 6, 5, 9, 9, 6, 1, 10, 1, 7, 5, 7, 5, 4, 8, 2, 4, 8, 6, 3, 4, 2, 4, 6, 8, 1, 3, 5, 21, 7, 3, 6, 10, 4, 4, 10, 3, 5, 7, 8, 9, 7, 5, 8, 24, 18, 4, 3, 4, 7, 5, 13, 3, 2, 7, 16, 8, 8, 11, 6, 5, 9, 5, 0, 9, 5, 5, 5, 27, 7, 8, 7, 19, 8, 5, 7, 6, 7, 7, 4, 6, 5, 4, 6, 6, 4, 6, 5, 3, 3, 6, 4, 18, 13, 10, 4, 45, 11, 8, 6, 2, 4, 23, 4, 7, 7, 29, 7, 8, 6, 3, 9, 4, 8, 2, 8, 5, 5, 7, 3, 3, 6, 11, 9, 16, 3, 1, 4, 19, 7, 4, 5, 4, 9, 14, 4, 3, 8, 6, 8, 6, 6, 7, 5, 8, 9, 4, 6, 8, 16, 9, 4, 0, 4, 10, 19, 13, 4, 37, 8, 4, 1, 4, 4, 5, 9, 7, 9, 8, 4, 8, 8, 1, 9, 5, 3, 6, 2, 26, 3, 7, 3, 1, 5, 7, 5, 5, 4, 8, 3, 3, 9, 8, 4, 2, 6, 4, 6, 6, 8, 7, 11, 12, 3, 5, 11, 10, 4, 19, 11, 9, 23, 16, 7, 5, 3, 12, 6, 8, 12, 5, 3, 7, 5, 6, 6, 9, 3, 6, 28, 2, 5, 4, 3, 6, 5, 36, 8, 26, 7, 2, 4, 6, 5, 9, 3, 9, 3, 5, 3, 11, 2, 13, 1, 3, 9, 5, 9, 4, 4, 3, 7, 8, 5, 21, 8, 4, 10, 1, 7, 7, 7, 26, 3, 6, 7, 7, 6, 9, 3, 6, 5, 2, 10, 3, 4, 17, 4, 4, 7, 3, 14, 9, 8, 1, 8, 6, 5, 8, 1, 6, 5, 7, 2, 6, 6, 3, 9, 9, 10, 9, 8, 7, 4, 6, 10, 5, 23, 8, 4, 6, 6, 5, 60, 6, 5, 6, 5, 7, 8, 1, 9, 9, 1, 2, 1, 26, 5, 6, 7, 9, 3, 3, 9, 8, 10, 6, 9, 5, 24, 6, 5, 12, 6, 5, 4, 3, 7, 5, 3, 3, 7, 7, 1, 5, 2, 5, 5, 3, 7, 6, 8, 4, 3, 8, 3, 4, 7, 10, 2, 5, 9, 5, 6, 7, 2, 2, 7, 5, 6, 6, 8, 6, 9, 3, 6, 28, 9, 8, 3, 5, 16, 4, 3, 1, 10, 32, 7, 3, 23, 8, 1, 7, 22, 8, 6, 3, 24, 4, 10, 4, 31, 10, 10, 4, 18, 1, 4, 4, 6, 3, 11, 4, 6, 5, 1, 4, 24, 9, 6, 2, 5, 16, 1, 7, 5, 18, 8, 4, 7, 14, 10, 6, 7, 3, 5, 2, 4, 3, 1, 6, 8, 1, 3, 11, 5, 7, 6, 9, 4, 8, 5, 8, 12, 6, 3, 1, 10, 8, 4, 6, 7, 6, 4, 5, 5, 8, 6, 5, 2, 6, 4, 11, 9, 11, 5, 6, 9, 4, 5, 3, 6, 10, 13, 7, 6, 4, 5, 1, 9, 6, 11, 7, 8, 3, 11, 7, 15, 25, 4, 8, 2, 0, 1, 7, 8, 1, 4, 4, 1, 6, 8, 7, 27, 5, 3, 7, 6, 8, 17, 4, 15, 3, 4, 13, 5, 21, 2, 5, 5, 5, 4, 6, 9, 21, 2, 2, 3, 11, 11, 6, 6, 3, 6, 7, 4, 3, 5, 5, 1, 18, 11, 17, 4, 10, 0, 4, 9, 8, 7, 3, 3, 5, 8, 8, 8, 8, 5, 3, 4, 27, 9, 2, 5, 4, 5, 3, 22, 2, 8, 3, 7, 4, 6, 7, 4, 9, 3, 3, 4, 3, 5, 4, 8, 7, 3, 4, 7, 5, 10, 5, 3, 5, 5, 4, 12, 6, 19, 9, 7, 5, 6, 5, 9, 10, 7, 4, 7, 10, 6, 2, 1, 4, 7, 8, 5, 7, 7, 5, 4, 5, 1, 8, 8, 6, 2, 3, 7, 4, 7, 6, 5, 11, 6, 7, 4, 3, 4, 7, 5, 7, 2, 6, 10, 0, 9, 9, 3, 7, 5, 2, 3, 8, 6, 3, 4, 7, 4, 16, 5, 2, 17, 2, 2, 6, 8, 7, 4, 4, 3, 5, 10, 8, 6, 5, 3, 5, 11, 2, 9, 1, 5, 0, 5, 5, 1, 11, 4, 4, 8, 5, 5, 20, 20, 7, 2, 4, 5, 1, 2, 7, 12, 8, 25, 5, 2, 7, 7, 3, 8, 8, 4, 6, 10, 8, 5, 7, 0, 6, 7, 6, 4, 17, 4, 8, 6, 4, 10, 4, 4, 6, 7, 6, 4, 4, 9, 5, 6, 5, 7, 2, 4, 5, 7, 5, 61, 9, 6, 4, 6, 8, 11, 4]
mean = numpy.mean(vector)
std = numpy.std(vector)
variance = std * std

def relevance_score(x):
    probability = (1 + math.erf((x - mean)/math.sqrt(2 * std**2)))
    def get_probability(x, m, v):
        return ((1 / math.sqrt(2 * v * 3.14)) * math.exp(-1 * (x - m) * (x - m) / (2 * v)))
    print get_probability(4, mean, variance)
    return get_probability(4, mean, variance)

g = Goose()
app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

keyword_dictionary = []

def read_auto_keywords():
    print('reading in auto generated keywords ...')
    with open('auto_keywords.txt', 'r') as data_file:
        for line in data_file:
            keyword_dictionary.append(line.rstrip())

import os.path
if not os.path.isfile('auto_keywords.txt'):
    print('generating auto keywords ...')
    from extract_keywords import create_keyword_file
    create_keyword_file()
read_auto_keywords()
with open('keywords.txt', 'r') as data_file:
    print('reading hardcoded keywords ....')
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

class KeywordList(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String)

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

@app.route('/jumbotron_files/<path:path>')
def send_js(path):
    return send_from_directory('jumbotron_files', path)

@app.route('/', methods=['GET'])
def index():
    return render_template('jumbotron.html')
    #return "Hello, World!"

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
            x = len(keywords)
            print('calculating relevancy score ...')
            is_relevant = relevance_score(x)
            print(str(is_relevant))
            input_data = Data(url=url, text=text, title=title, relevancy = is_relevant, keywords=str(keywords))
            db.session.add(input_data)
            db.session.commit()
        if disable_text == '1':
            text = None
        data = {'id': input_data.id, 'title': title, 'text': text, 'relevancy': "{0:.2f}".format(float(is_relevant)), 'keywords': keywords, 'feedback': input_data.feedback_relevancy}
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
