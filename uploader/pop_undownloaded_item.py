from app.connect_database import Connect


def pop_undownloaded_item(limit):
    query = {'category': "Image Set", "file_count_matches": {"$exists": False},
             'ex.archiver_key': {"$exists": True}}
    result = Connect.get_connection().Gallery.find(query).sort([("ex.upload_time", -1)]).limit(limit)
    return result
