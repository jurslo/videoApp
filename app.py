"""
Main file of the app
"""

from flask import Flask, render_template, request

from database import db_get_videos, db_sync_from_manifest

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    sort_by = request.form.get('sort-by', 'unsorted')
    videos = db_get_videos()
    if sort_by == 'name':
        videos.sort(key=lambda item: item['name'])
    return render_template("base.html", videos=videos, sort_by=sort_by)


if __name__ == '__main__':
    db_sync_from_manifest()
    app.run(debug=True)
