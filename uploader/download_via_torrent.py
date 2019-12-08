# import sys
# import os
# import time
#
# session = libtorrent.session()
# session.set_alert_queue_size_limit(1024 * 1024)
# session.listen_on(6881, 6881)
# torrent_info = libtorrent.torrent_info('/home/kyle/bt/1.torrent')
# add_params = {
#     'save_path': '/home/kyle/bt/',
#     'storage_mode': libtorrent.storage_mode_t.storage_mode_sparse,
#     'paused': False,
#     'auto_managed': True,
#     'ti': torrent_info,
#     # 如果是磁力链接，就用 url 替代 ti 参数
#     # 'url': 'magnet:?xt=urn:btih:69bda373e8e3e0c59428bfb90c5df8c50603d751&amp;tr=udp://9.rarbg.to:2710/announce',
# }
# handle = session.add_torrent(add_params)
# session.start_dht()
#
# alert = session.pop_alert()
# while alert:
#     print
#     '[alert msg]: %s' % alert.message()
#     alert = session.pop_alert()
# state_str = ['queued', 'checking', 'downloading metadata', \
#              'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
#
# # 阻塞下载
# while not (handle.is_seed()):
#     s = handle.status()
#     print
#     '\ractive_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
#     (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#      s.num_peers, s.num_seeds, state_str[s.state]),
#     sys.stdout.flush()
#     time.sleep(0.2)
# # 下载完后开始做种
# handle.super_seeding()
#
# # 阻塞输出做种状态
# seedtime = 1000
# while seedtime & gt; 0:
#     seedtime -= 1
#     s = handle.status()
#     print
#     '\rseed_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
#     (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#      s.num_peers, s.num_seeds, state_str[s.state]),
#     sys.stdout.flush()
#     time.sleep(1)