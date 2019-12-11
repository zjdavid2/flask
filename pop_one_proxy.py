import requests
from config import Config


def pop_one_proxy() -> str:
    r = requests.get(Config.PROXY_URL)
    print("Pulled one proxy from server")
    proxy = r.json()['data']['proxy_list'][0]
    proxy_with_credential = "http://%(user)s:%(pwd)s@%(proxy)s/" % {'user': Config.PROXY_USERNAME,
                                                                    'pwd': Config.PROXY_PASSWORD,
                                                                    'proxy': proxy}
    return proxy_with_credential
