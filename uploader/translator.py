import os
import glob
from app.connect_database import Connect
from bson.objectid import ObjectId

zip_list = [f for f in glob.glob("*.zip")]  # 获取本目录下的所有zip文件

for zip_index, zip_file_name in enumerate(zip_list):
    object_id = os.path.splitext(zip_file_name)[0]
    local_db = Connect.get_local_connection()
    record = local_db.Gallery.find_one({'_id': ObjectId(object_id)})
    print(record)
