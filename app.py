"""
Main file of the app
"""

from flask import Flask, render_template, request

from database import db_get_videos, db_sync_from_manifest, db_get_all_features

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    sort_by = request.form.get('sort-by', 'unsorted')
    feature_names = db_get_all_features()
    features = {}
    for ftr in feature_names:
        features[ftr] = (request.form.get(f'ftr-{ftr}', 'off') == 'on')
    videos = db_get_videos([ftr for (ftr, present) in features.items() if present], sort_by == 'name')
    return render_template("base.html", videos=videos, sort_by=sort_by, features=features)


if __name__ == '__main__':
    db_sync_from_manifest()
    app.run(debug=True)
