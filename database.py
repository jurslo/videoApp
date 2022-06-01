"""
Database API and helper functions
"""

import logging
import sqlite3 as sl

import requests

from config import config


def db_create_tables(con):
    con.execute('''
        CREATE TABLE IF NOT EXISTS video (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            short_name TEXT,
            icon_uri TEXT,
            manifest_uri TEXT,
            source TEXT,
            focus TINYINT(1),
            disabled TINYINT(1),
            extra_text TEXT,
            certificate_uri TEXT,
            description TEXT,
            is_featured TINYINT(1),
            drm TEXT,
            license_servers TEXT,
            license_request_headers TEXT,
            request_filter TEXT,
            response_filter TEXT,
            clear_keys TEXT,
            extra_config TEXT,
            ad_tag_uri TEXT,
            ima_video_id TEXT,
            ima_asset_key TEXT,
            ima_content_src_id INTEGER,
            mime_type TEXT,
            media_playlist_full_mime_type TEXT,
            stored_progress INTEGER,
            stored_content TEXT
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS feature (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS video_feature (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER NOT NULL,
            feature_id INTEGER NOT NULL
        )
    ''')


def db_drop_tables(con):
    con.execute('DROP TABLE IF EXISTS video')
    con.execute('DROP TABLE IF EXISTS feature')
    con.execute('DROP TABLE IF EXISTS video_feature')


def db_add_video(con, video):
    cur = con.cursor()

    sql = '''
        INSERT INTO video(name, short_name, icon_uri, manifest_uri, source, focus, disabled, extra_text,
            certificate_uri, description, is_featured, drm, license_servers, license_request_headers, request_filter,
            response_filter, clear_keys, extra_config, ad_tag_uri, ima_video_id, ima_asset_key, ima_content_src_id,
            mime_type, media_playlist_full_mime_type, stored_progress, stored_content)
        VALUES(:name, :shortName, :iconUri, :manifestUri, :source, :focus, :disabled, :extraText, :certificateUri,
            :description, :isFeatured, :drm, :licenseServers, :licenseRequestHeaders, :requestFilter, :responseFilter,
            :clearKeys, :extraConfig, :adTagUri, :imaVideoId, :imaAssetKey, :imaContentSrcId, :mimeType,
            :mediaPlaylistFullMimeType, :storedProgress, :storedContent)
    '''

    cur.execute(sql, video)

    return cur.lastrowid


def db_get_feature_id_by_name(con, name):
    for row in con.execute('SELECT id FROM feature WHERE name = ?', (name,)):
        return row[0]
    return None


def db_add_or_get_feature(con, feature_name):
    cur = con.cursor()

    feature_id = db_get_feature_id_by_name(con, feature_name)
    if feature_id is None:
        cur.execute('INSERT INTO feature(name) VALUES(?)', (feature_name,))
        feature_id = cur.lastrowid
    return feature_id


def db_add_video_feature(con, video_id, feature_id):
    con.execute('INSERT INTO video_feature(video_id, feature_id) VALUES(?, ?)', (video_id, feature_id))


def db_add_video_feature_name(con, video_id, feature_name):
    feature_id = db_add_or_get_feature(con, feature_name)
    db_add_video_feature(con, video_id, feature_id)


def db_get_videos():
    con = sl.connect(config['database_name'])
    videos = []
    for row in con.execute('SELECT name, icon_uri FROM video WHERE disabled = 0'):
        vid = {
            'name': row[0],
            'iconUri': row[1],
        }
        videos.append(vid)
    con.close()
    return videos


def db_init_from_manifest(videos):
    con = sl.connect(config['database_name'])
    db_drop_tables(con)
    db_create_tables(con)
    for vid in videos:
        logging.debug('Sync: Processing video: %s', vid["name"])
        for key in ['extraText', 'drm', 'licenseServers', 'licenseRequestHeaders', 'clearKeys', 'extraConfig',
                    'storedContent']:
            if key in vid:
                vid[key] = str(vid[key])
            else:
                vid[key] = None
        for key in ['name', 'shortName', 'iconUri', 'manifestUri', 'source', 'focus', 'disabled', 'certificateUri',
                    'description', 'isFeatured', 'requestFilter', 'responseFilter', 'adTagUri', 'imaVideoId',
                    'imaAssetKey', 'imaContentSrcId', 'mimeType']:
            if key not in vid:
                vid[key] = None
        video_id = db_add_video(con, vid)
        if 'features' in vid:
            for feature_name in vid['features']:
                db_add_video_feature_name(con, video_id, feature_name)
    con.commit()
    con.close()


def db_get_videos_manifest():
    r = requests.get(config['videos_manifest_url'])
    r.raise_for_status()
    return r.json()


def db_sync_from_manifest():
    logging.info('Syncing video manifest to local database')
    videos = db_get_videos_manifest()
    db_init_from_manifest(videos)
    logging.info('Finished syncing video manifest to local database')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    db_sync_from_manifest()
