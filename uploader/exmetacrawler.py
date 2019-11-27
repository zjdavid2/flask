#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import io
import re
import time
import requests

cookie = "ipb_member_id=9999999;ipb_pass_hash=ffffffffffffffff"

oldestTimestamp = int(time.time())
nextLatestTimestamp = 0

reqpy = {"method": "gdata", "gidlist": [[639967, "e2be237948"]], "namespace": 1}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
                  'Safari/537.36',
    "Accept": "application/jsonrequest",
    "Content-type": "text/json",
    "Cookie": cookie
}

headers4search = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
                  'Safari/537.36',
    "Accept": "application/jsonrequest",
    "Content-type": "*/*",
    "Cookie": cookie
}

respJs = {}


def getSearchHtml(page):
    r = requests.get('https://exhentai.org', params={'page': str(page), 'f_cats': 0,
                                                     'f_sname': 'on'}, headers=headers)

    if r.status_code != 200:
        print("ERROR while getting search result!")
        print("Will retry after 5s...")
        time.sleep(5)
        return getSearchHtml(page)
    return r.text


def setlist(htmldoc):
    gurls = re.findall("/g/[0-9]+/[0-9a-zA-Z]+/", htmldoc)
    print(gurls)
    global reqpy
    gidlist = []
    for url in gurls:
        a1, a2, a3, a4, a5 = url.split('/')
        a3 = int(a3)
        gidlist.append([a3, a4])
    print(gidlist)
    reqpy['gidlist'] = gidlist


def process():
    global oldestTimestamp, reqpy, headers, respJs, nextLatestTimestamp

    req = json.dumps(reqpy)
    r = requests.post('https://exhentai.org/api.php', data=req, headers=headers)
    print(r.text)

    if r.status_code != 200:
        print("ERROR while getting search result!")
        print("Will retry after 5s...")
        time.sleep(5)
        return process()

    response = r.json()
    print(r.json())
    glist = response['gmetadata']
    for i in range(len(glist)):
        if int(glist[i]['posted']) < oldestTimestamp:
            oldestTimestamp = int(glist[i]['posted'])
        if int(glist[i]['posted']) > nextLatestTimestamp:
            nextLatestTimestamp = int(glist[i]['posted'])
        respJs[glist[i]['gid']] = glist[i]


def write_tmp(output_file):
    global respJs
    with io.open(output_file, "w", encoding="utf-8") as outf:
        outf.write(json.dumps(respJs, ensure_ascii=False))


def main(latest_posted):
    global nextLatestTimestamp, cookie, headers4search, headers
    # latest_posted = 1574553600
    ipb_member_id = "4944111"
    ipb_pass_hash = "efe917bf782e16c80463e9dc5ac7c105"
    outputfile = "gdata.json"

    cookie = ("ipb_member_id=" + str(ipb_member_id) + ";ipb_pass_hash=" + str(ipb_pass_hash))
    headers4search['Cookie'] = cookie
    headers['Cookie'] = cookie

    print("Latest gallery given was posted at " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(latest_posted)))
    nextLatestTimestamp = latest_posted
    page = 0
    global oldestTimestamp
    while oldestTimestamp > latest_posted:
        print("Now oldest " + str(oldestTimestamp) + " > " + str(latest_posted))
        print("Requesting search page " + str(page + 1) + "...")
        search_html = getSearchHtml(page)
        setlist(search_html)
        process()
        page += 1
    print("Done. We ve got gallery posted at " + str(oldestTimestamp) + " <= " + str(latest_posted))

    print("Writing json to file " + outputfile + "...")
    write_tmp(outputfile)


if __name__ == '__main__':
    main(0)
