#!/usr/bin/env python

from flask import Flask,render_template
from flask import jsonify, request
from flask_cors import CORS,cross_origin
from flask import Response
from textblob import TextBlob, Word
from profanity_filter import ProfanityFilter

pf = ProfanityFilter()
profane_words_file = open("./profane_words2", 'r')
profane_words = {str(line[:-1]) for line in profane_words_file.readlines()}
pf.custom_profane_word_dictionaries = {'en': profane_words}

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/auto_correction', methods=["POST"])
def predict():
    sug_words = {}
    profane_words = []
    text = request.json['text'].split()
    for i in text:
        i = i.lower()
        if(pf.censor_word(i).original_profane_word is not None):
            profane_words.append(pf.censor_word(i).original_profane_word)
    for i in text:
        if(Word(i).spellcheck()[0][1]<1.0):
            sug_words[i] = []
            for j in Word(i).spellcheck()[:3]:
                sug_words[i].append(j[0])
    return jsonify({'Suggested_Words': sug_words, "Profane_Words": profane_words})


if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=True, port=5000)
