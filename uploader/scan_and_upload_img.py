import glob
import re
import zipfile
import os
import shutil
import requests
import hashlib
import logging
import threading


class ScanAndUpload:
    base_url = 'https://dd.works'
    view_url = base_url + '/v1/view/getDetail'
    upload_url = base_url + '/v1/upload/directUpload'
    login_url = base_url + '/v1/auth'
    logging.basicConfig(filename='uploader.log', level=logging.DEBUG)
    logger = logging.getLogger()
    success = 0
    total = 0

    def sha1(self, this_file_name):
        hash_sha1 = hashlib.sha1()
        with open(this_file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()

    def login(self, username, password):
        login_url = self.base_url + '/v1/auth/login'
        r = requests.post(login_url, data={'username': username, 'password': password})
        print(r.json())
        return r.json()['jwt']

    def move_to_failed(self, file_to_move):
        if not os.path.exists('failed'):
            os.makedirs('failed')
        try:
            shutil.move(file_to_move, 'failed/' + file_to_move)
        except:
            logging.error('Failed to move ' + file_to_move + ' to failed.')

    def move_to_warning(self, file_to_move):
        if not os.path.exists('warning'):
            os.makedirs('warning')
        try:
            shutil.move(file_to_move, 'warning/' + file_to_move)
        except:
            logging.error('Failed to move ' + file_to_move + ' to warning.')

    def move_to_completed(self, file_to_move):
        if not os.path.exists('completed'):
            os.makedirs('completed')
        try:
            shutil.move(file_to_move, 'completed/' + file_to_move)
        except:
            logging.error('Failed to move ' + file_to_move + ' to completed.')

    def upload_one(self, hash_id, title, file_name, index, zip_file_name, zip_index, headers):
        upload_complete_url = self.upload_url + '/' + hash_id + '/' + str(index)
        file = open(os.path.join(title, file_name), 'rb')
        file_hash = self.sha1(os.path.join(title, file_name))
        files = {'file': file}
        try:
            r_upload = requests.post(upload_complete_url, files=files, data={'sha1': file_hash}, headers=headers)
        except:
            logging.error(file_name + ' upload failed.')
            self.move_to_failed(zip_file_name)
            return
        self.total += 1
        try:
            json = r_upload.json()
            if json['msg'] == 'Img successfully uploaded':
                self.success += 1
            else:
                logging.warning(json)
                self.move_to_warning(zip_file_name)
        except:
            logging.error(r_upload.text)
            self.move_to_failed(zip_file_name)
        info_log = 'Zip Index ' + str(zip_index) + ', total success ' + str(self.success) + '/' + str(self.total)
        print(info_log)
        logging.info(info_log)
        self.logger.handlers[0].flush()

    def upload_all_in_directory(self):
        jwt_token = self.login('zjdavid', 'torsan89')
        headers = {'auth': jwt_token}

        zip_list = [f for f in glob.glob("*.zip")]  # 获取本目录下的所有zip文件

        for zip_index, zip_file_name in enumerate(zip_list):
            title_with_order = re.split('\\.zip', zip_file_name)[0]
            title = re.sub('[0-9]+\\.', '', title_with_order, count=1)
            logging.info('Uploading: ' + title)
            print(title)
            try:
                with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
                    r = requests.get(self.view_url, {'japanTitle': title}, headers=headers)
                    hash_id = r.json().get('_id')
                    if hash_id is None:
                        r2 = requests.get(self.view_url, {'title': title}, headers=headers)
                        hash_id = r2.json().get('_id')
                    if hash_id is None:  # IF still not found
                        logging.error('Failed to upload one, record not found: ' + zip_file_name)
                        self.move_to_failed(zip_file_name)
                        shutil.rmtree(title, ignore_errors=True)
                        continue

                    zip_ref.extractall(title)  # 解压到标题目录
                    thread_list = []

                    for index, file_name in enumerate(sorted(os.listdir(title))):
                        t = threading.Thread(target=self.upload_one, args=(hash_id, title, file_name, index,
                                                                           zip_file_name, zip_index, headers))
                        thread_list.append(t)
                    for thread in thread_list:
                        thread.start()
                    for thread in thread_list:
                        thread.join()
                    self.move_to_completed(zip_file_name)
                    shutil.rmtree(title, ignore_errors=True)
            except zipfile.BadZipFile:
                logging.error(zip_file_name + ' is not a valid zip file.')
                self.move_to_failed(zip_file_name)
            except Exception as ex:
                logging.error(zip_file_name + ' encountered an error.')
                logging.error(ex)
                self.move_to_failed(zip_file_name)


if __name__ == '__main__':
    ScanAndUpload().upload_all_in_directory()
