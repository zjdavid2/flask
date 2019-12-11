import requests
from bs4 import BeautifulSoup
import os
from pop_one_proxy import pop_one_proxy
from uploader.pop_undownloaded_item import pop_undownloaded_item
from uploader.scan_and_upload_img import ScanAndUpload
from config import Config
from requests.exceptions import *
from app.connect_database import Connect
from bson import ObjectId

proxy_list = []


def get_proxy_list():
    proxy_with_credential = pop_one_proxy()
    global proxy_list
    proxy_list = [proxy_with_credential]


def download_using_archiver_key(record):
    if not proxy_list:
        get_proxy_list()
    try:
        print(record['_id'])
        ex = record['ex']
        if ex.get('archiver_key') is None:
            return  # Archiver key not found.
        archiver_key = ex['archiver_key'].replace('--', '-', 1)
        proxies = {
            "http": proxy_list[0],
            "https": proxy_list[0],
        }
        url = 'https://exhentai.org/archiver.php?gid=' + ex['gid'] + '&token=' + ex['token'] + '&or=' + archiver_key
        # data = 'dltype=org&dlcheck=Download+Original+Archive'
        data = {'dtype': 'org', 'dlcheck': 'Download Original Archive'}
        cookie = {'ipb_member_id': Config.IPB_MEMBER_ID, 'ipb_pass_hash': Config.IPB_PASS_HASH, 'igneous': 'c3737b9c2'}
        r = requests.post(url, data=data, cookies=cookie, proxies=proxies, timeout=15)
        if 'Your IP address has been temporarily banned for excessive pageloads' in r.text:
            raise ProxyError
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.prettify())
        next_url = soup.find_all('a')[0].get('href') + '?start=1'
        file_name = download_file(next_url)
        new_name = str(record['_id']) + '.zip'
        os.rename(file_name, str(record['_id']) + '.zip')
        print('Created: ' + new_name)
        return new_name
    except (ConnectTimeout, ProxyError, ConnectionRefusedError,
            Timeout, ReadTimeout, SSLError) as error:  # This proxy fails.
        proxy_list.pop(0)
        print(error)
        print('Pop one from proxy list.')
        if not proxy_list:
            get_proxy_list()
        download_using_archiver_key(record)  # retry=
    except HTTPError as err:
        if err.response.status_code == 410:
            print(err.response.text)
            Connect.get_connection().Gallery.update_one({'_id': ObjectId(record['_id'])},
                                                        {'$set': {'uploaded': True,
                                                                  'file_count_matches': True}})


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename


if __name__ == '__main__':
    get_proxy_list()
    print(proxy_list)
    ScanAndUpload().upload_all_named_hash_id_in_directory()
    while True:
        record = pop_undownloaded_item(1)[0]
        download_using_archiver_key(record)
        ScanAndUpload().upload_all_named_hash_id_in_directory()
