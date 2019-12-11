from app.connect_database import Connect


def update_gallery_tag_list():
    db = Connect.get_connection()
    for record in db.Gallery.find():
        tags: dict = record['tags']
        tag_dict = list()
        for category, tag_arr in tags.items():
            if not isinstance(tag_arr, list):
                continue
            for tag in tag_arr:
                if not isinstance(tag, list) or len(tag) < 2 or tag[1] < 100:
                    continue  # Tag[1] is the confidence score. less than 100 is not searchable
                tag_dict.append(category + ':' + tag[0])
        db.Gallery.update_one({'_id': record['_id']}, {'$set': {'tag_dict': tag_dict}})


if __name__ == '__main__':
    update_gallery_tag_list()
