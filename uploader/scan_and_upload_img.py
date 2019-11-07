import glob
import re
import zipfile
import os
import shutil
import requests

base_url = 'http://127.0.0.1:5000'
view_url = base_url + '/v1/view/getDetail'
upload_url = base_url + '/v1/upload/directUpload'

zip_list = [f for f in glob.glob("*.zip")]  # 获取本目录下的所有zip文件
for zip_file_name in zip_list:
    title_with_order = re.split('\\.zip', zip_file_name)[0]
    title = re.sub('[0-9]+\\.', '', title_with_order, count=1)
    print(title)
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall(title)  # 解压到标题目录
        r = requests.get(view_url, {'japanTitle': title})
        hash_id = r.json()['_id']
        if hash_id is None:
            continue
        print(r.json())
        for index, file in enumerate(sorted(os.listdir(title))):
            upload_complete_url = upload_url + '/' + hash_id + '/' + str(index)
            files = {'file': open(os.path.join(title, file), 'rb')}
            r_upload = requests.post(upload_complete_url, files=files)
            print(r_upload.json())

        shutil.rmtree(title, ignore_errors=True)


