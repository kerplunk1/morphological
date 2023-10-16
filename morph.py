import pymorphy3
from inflect import PhraseInflector
from flask import Flask, request
import json
from autocorrect import Speller


app = Flask(__name__)


@app.route('/all', methods=['GET', 'POST'])
def morphling_and_correct():
    data = request.get_json()
    phrase = data['phrase']
    form = data['form']

    spell = Speller('ru', fast=True)
    text = spell(phrase)

    morph = pymorphy3.MorphAnalyzer()
    inflector = PhraseInflector(morph)

    return json.dumps({"result": inflector.inflect(text, form)}, ensure_ascii=False), 200, {'Content-Type':'text/json; charset=utf-8'}


@app.route('/case_declensions', methods=['GET', 'POST'])
def morphling():
    data = request.get_json()
    phrase = data['phrase']
    form = data['form']

    morph = pymorphy3.MorphAnalyzer()
    inflector = PhraseInflector(morph)

    return json.dumps({"result": inflector.inflect(phrase, form)}, ensure_ascii=False), 200, {'Content-Type':'text/json; charset=utf-8'}


@app.route('/correct_mistake', methods=['GET', 'POST'])
def correct():
    data = request.get_json()
    phrase = data['phrase']

    spell = Speller('ru', fast=True)
    text = spell(phrase)

    return json.dumps({"result": text}, ensure_ascii=False), 200, {'Content-Type':'text/json; charset=utf-8'}


if __name__ == '__main__':
    app.run()
