from flask import Flask, render_template, request
import spacy
import requests
from bs4 import BeautifulSoup
import nltk
import spacy
import pytextrank

nltk.download('stopwords')

app = Flask(__name__)


def get_wiki_content(url):
    req_obj = requests.get(url.strip())
    text = req_obj.text
    soup = BeautifulSoup(text)
    all_paras = soup.find_all("p")
    wiki_text = ''
    for para in all_paras:
        wiki_text += para.text
    return wiki_text


def text_rank_test(url, x, y):
    example_text = get_wiki_content(url)
    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe("textrank")
    doc = nlp(example_text)

    summary = []
    for sent in doc._.textrank.summary(limit_phrases=x, limit_sentences=y):
        summary.append(sent)

    summary_final = " ".join(str(x) for x in summary)
    return summary_final, example_text, len(example_text), len(summary_final)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        url = request.form.get("url")
        x = request.form.get("phrases_limit")
        y = request.form.get("sentence_limit")
        x1 = int(x)
        y1 = int(y)
        summary_final, example_text, len_example_text, len_summary_final = text_rank_test(
            url, x1, y1)
    return render_template("summary.html", summary=summary_final, original_txt=example_text, len_original_txt=len_example_text, len_summary=len_summary_final)


if __name__ == "__main__":
    app.run(debug=True)
