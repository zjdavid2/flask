import celery
from bson import ObjectId
from app import connect_database
from uploader.download_using_archiver_key import download_using_archiver_key
from uploader.scan_and_upload_img import ScanAndUpload


@celery.task(bind=True)
def download_gallery_with_object_id(self, object_id_str: str, origin_url: str):
    self.update_state(state='PROGRESS',
                      meta={'status': 'starting'})
    object_id = ObjectId(object_id_str)
    record = connect_database.Connect.get_connection().Gallery.find_one({'_id': object_id})
    self.update_state(state='PROGRESS',
                      meta={'status': 'downloading'})
    download_using_archiver_key(record)
    self.update_state(state='PROGRESS',
                      meta={'status': 'uploading'})
    ScanAndUpload().upload_all_named_hash_id_in_directory()
    return {'status': 'COMPLETED', 'url': origin_url}
