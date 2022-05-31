"""
Main file of the app
"""

from flask import Flask, render_template, request
import requests

from config import config

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    sort_by = request.form.get('sort-by', 'unsorted')
    videos = get_videos()
    if sort_by == 'name':
        videos.sort(key=lambda item: item['name'])
    return render_template("base.html", videos=videos, sort_by=sort_by)


def get_videos():
    r = requests.get(config['videos_manifest_url'])
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    app.run(debug=True)
