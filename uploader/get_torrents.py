import requests
from uploader import pop_undownloaded_item
from bs4 import BeautifulSoup


def get_proxy():
    # 隧道服务器
    tunnel_host = "tps189.kdlapi.com"
    tunnel_port = "15818"

    # 隧道id和密码
    username = "zjdavid.2003"
    password = "h9cx36wg"
    r = requests.get(
        'https://dps.kdlapi.com/api/getdps/?orderid=987569609393130&num=1&pt=1&format=json&sep=1')
    proxy = r.json()['data']['proxy_list'][0]
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                        'proxy': proxy},
        "https": "https://%(user)s:%(pwd)s@%(proxy)s/" % {'user': username, 'pwd': password,
                                                          'proxy': proxy}
    }
    return proxies


def download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename


def main():
    record_list = pop_undownloaded_item.pop_undownloaded_item(10)
    proxies = get_proxy()
    for record in record_list:
        gid = record['ex']['gid']
        token = record['ex']['token']
        cookie = {'ipb_member_id': '4944111', 'ipb_pass_hash': 'efe917bf782e16c80463e9dc5ac7c105', 'igneous': 'c3737b9c2'}
        url = 'https://exhentai.org/gallerytorrents.php?gid=' + gid + '&t=' + token
        proxy = get_proxy()
        print(proxy)
        r = requests.get(url, proxies=proxies, cookies=cookie)
        # print(BeautifulSoup(r.text).prettify())
        soup = BeautifulSoup(r.text)
        torrent_address_tag = soup.a
        # print(soup.prettify())
        if torrent_address_tag:
            address = torrent_address_tag.get('href')
            obj_id = str(record['_id'])
            download_file(address, obj_id + '.torrent')
            print(address)


if __name__ == '__main__':
    main()
