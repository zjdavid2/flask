from app.connect_database import Connect
import json


# {'language': [], 'character': [], 'female': [], 'male': [], 'group': [], 'artist': [['mmm', 150]],
# 'misc': [], 'parody': []}  <-- Sample data
connection = Connect.get_connection()


def write_tmp(dict_file):
    with open('output.json', "w") as outf:
        outf.write(json.dumps(dict_file))


def update_tags_list():
    tags_dict = list()
    for record in connection.Gallery.find():
        for category, tags in record['tags'].items():
            tag: list  # [name, confidence]
            for tag in tags:
                if not isinstance(tag, list) or len(tag) == 0:
                    continue
                tag_name = tag[0]
                insert_one(tag_name, category)

    # write_tmp(tags_dict)
    # print(tags_dict)
    # for record in tags_dict:
    #     connection.tags.insert_one(record)


def insert_one(tag_name, category):
    try:
        existing_record = contains(tag_name, category)
        if existing_record is not None:
            connection.tags.update_one({'_id': existing_record['_id']},
                                       {'$set': {'occurrences': existing_record['occurrences'] + 1}})
        else:
            connection.tags.insert_one(dict(category=category, name=tag_name, occurrences=1))
    except:
        print('Failed. Retrying...')
        insert_one(tag_name, category)


def contains(tag_name, category):
    result = connection.tags.find_one({'category': category, 'name': tag_name})
    return result


def clear_occurrences():
    Connect.get_connection().tags.update_many({}, {'$set': {'occurrences': 0}})


# def index_of(tag_name: str, tag_dict: list) -> int:
#     for (index, record) in enumerate(tag_dict):
#         if record['name'] == tag_name:
#             return index
#     return -1


if __name__ == '__main__':
    update_tags_list()
    # clear_occurrences()
