import json
from app.connect_database import Connect
from datetime import datetime
import uploader.exmetacrawler as crawler
import re


db = Connect().get_connection()


def get_latest_record(limit):
    result = db.Gallery.find().sort([("ex.upload_time", -1)]).limit(limit)
    return result


latest_time: datetime = get_latest_record(1)[0]['ex']['upload_time']
latest_time_stamp = int(latest_time.timestamp())
crawler.main(latest_time_stamp)


def map_tags_into_list(tags):
    tags_cat_list = ['language', 'character', 'female', 'male', 'group', 'artist', 'misc', 'parody']
    original_list = dict()

    for tag in tags_cat_list:
        original_list[tag] = list()

    tag: str
    for tag in tags:
        tag_split = re.split(':', tag)
        if len(tag_split) < 2:
            continue  # Not valid
        if tag_split[0] in tags_cat_list:
            original_list[tag_split[0]] = [tag_split[1], 100]
    return original_list


with open('gdata.json', 'r') as f:
    data: dict = json.load(f)
    record: dict
    for _, record in data.items():
        tags_dict = map_tags_into_list(record.get('tags', []))

        gid: int = record.get('gid', 0)
        token: str = record.get('token', '')
        posted: int = int(record.get('posted', '0'))
        ex_info_dict = dict(page_link='https://exhenta.org/g/' + str(gid) + '/' + token,
                            gid=str(gid),
                            token=token,
                            upload_time=datetime.utcfromtimestamp(posted),
                            uploader=record.get('uploader', ''))

        formatted_record = dict(title=record.get('title', ''),
                                japan_title=record.get('title_jpn', ''),
                                category=record.get('category', ''),
                                rating=[float(record.get('rating', '0.00')), 100],
                                ipfs_url=' ',
                                thumbnail=' ',
                                uploader=' ',
                                upload_time=0,
                                file_count=record.get('filecount', 0),
                                ex=ex_info_dict,
                                tags=tags_dict)

        print(formatted_record)
        insertion_result = db.Gallery.replace_one({'ex.gid': str(gid)}, formatted_record, upsert=True)
