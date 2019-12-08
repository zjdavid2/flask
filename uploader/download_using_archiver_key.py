import requests
from bs4 import BeautifulSoup
import os
from uploader.pop_undownloaded_item import pop_undownloaded_item
from uploader.scan_and_upload_img import ScanAndUpload
from config import Config

proxy_list = []


def get_proxy_list():
    # 隧道服务器
    tunnel_host = "tps181.kdlapi.com"
    tunnel_port = "15818"

    # 隧道id和密码
    tid = "t17568051491391"
    password = "i0n6h7kc"

    proxy = "http://%s:%s@%s:%s/" % (tid, password, tunnel_host, tunnel_port)
    global proxy_list
    proxy_list = [proxy]
    # r = requests.get('https://dev.kdlapi.com/api/getproxy/?orderid=987495241559611&num=100&protocol=2&method=2&an_an=1&an_ha=1&sep=2')
    # proxy_list = r.text.splitlines()


def download_using_archiver_key(record):
    try:
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
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.prettify())
        next_url = soup.find_all('a')[0].get('href') + '?start=1'
        file_name = download_file(next_url)
        new_name = str(record['_id']) + '.zip'
        os.rename(file_name, str(record['_id']) + '.zip')
        print('Created: ' + new_name)
        return new_name
    except:  # This proxy fails.
        proxy_list.pop(0)
        print('Pop one from proxy list.')
        if not proxy_list:
            get_proxy_list()
        download_using_archiver_key(record)  # retry


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
    while True:
        record = pop_undownloaded_item(1)[0]
        download_using_archiver_key(record)
        ScanAndUpload().upload_all_named_hash_id_in_directory()
