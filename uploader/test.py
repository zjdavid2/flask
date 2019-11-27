import requests
import re
from uploader.scan_and_upload_img import login


zip_file_name = '27.Yui Shop 03.zip'
title_with_order = re.split('\\.zip', zip_file_name)[0]

base_url = 'https://dd.works'
view_url = base_url + '/v1/view/getDetail'

title = re.sub('[0-9]+\\.', '', title_with_order, count=1)
print(title)

jwt_token = login('zjdavid', 'torsan89')
headers = {'auth': jwt_token}

r = requests.get(view_url, {'title': title}, headers=headers)
print(r.json())
print(r.request.url)