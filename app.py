"""
Main file of the app
"""

import logging
from threading import Event, Thread

from flask import Flask, render_template, request
from requests.exceptions import ConnectionError as RequestsConnectionError, HTTPError, Timeout

from config import config
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


def video_manifest_refresh_thread(event):
    while not event.wait(config['video_manifest_refresh_interval']):
        try:
            db_sync_from_manifest()
        # When API is not available just continue with data we already have in database
        except (RequestsConnectionError, HTTPError, Timeout) as e:
            logging.warning(e, exc_info=True)


def main():
    db_sync_from_manifest()

    event = Event()
    thread = Thread(target=video_manifest_refresh_thread, args=(event,))
    thread.start()

    app.run(debug=True)

    # Stop the child thread
    event.set()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
