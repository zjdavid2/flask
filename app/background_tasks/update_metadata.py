import json
from app.connect_database import Connect
from datetime import datetime
import app.background_tasks.exmetacrawler as crawler
import re


db = Connect().get_connection()


def get_latest_record(limit):
    result = db.Gallery.find().sort([("ex.upload_time", -1)]).limit(limit)
    return result


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


def upload_metadata_using_json():
    latest_time: datetime = get_latest_record(1)[0]['ex']['upload_time']
    latest_time_stamp = int(latest_time.timestamp()) - 50000
    crawler.main(latest_time_stamp)

    record_list = list()
    with open('gdata_roll.json', 'r') as f:
        data: dict = json.load(f)
        record: dict
        for _, record in data.items():
            print(record)
            tags_dict = map_tags_into_list(record.get('tags', []))

            gid: int = record.get('gid', 0)
            token: str = record.get('token', '')
            posted: int = int(record.get('posted', '0'))
            # print(record.get('archiver_key', ''))
            ex_info_dict = dict(page_link='https://exhentai.org/g/' + str(gid) + '/' + token,
                                gid=str(gid),
                                token=token,
                                upload_time=datetime.utcfromtimestamp(posted),
                                uploader=record.get('uploader', ''),
                                archiver_key=record.get('archiver_key', ''),
                                expunged=record.get('expunged', False))

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
            record_list.append(formatted_record)
            # if len(record_list) >= 100:
            #     flush_formatted_record(record_list)
            #     record_list = list()
            existing_record: dict = db.Gallery.find_one({'ex.gid': str(gid)})
            if existing_record is not None:
                print("Find existing record")
                existing_record.update(formatted_record)
                db.Gallery.replace_one({'ex.gid': str(gid)}, existing_record)
            else:
                db.Gallery.replace_one({'ex.gid': str(gid)}, formatted_record, upsert=True)
            # print(insertion_result)


def flush_formatted_record(record_list: list):
    db.Gallery.insert_many(record_list)


if __name__ == '__main__':
    upload_metadata_using_json()
    # add_archiver_key()
