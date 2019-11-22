class RequestError(object):
    def __init__(self, name=''):
        self.name = name

    def required_parameter_not_found(self):
        error_description = self.name + ' is a required parameter'
        return error_description

    def parameter_invalid(self):
        return self.name + ' is invalid.'

    @staticmethod
    def file_number_too_big():
        return 'Your image order number is larger than the expected file count.'

    @staticmethod
    def record_not_found():
        return 'Unable to find the record you are looking for.'

    @staticmethod
    def no_unique_parameter():
        return 'You must provide one unique parameter.'

    @staticmethod
    def invalid_hash_id():
        return 'Your hash ID is invalid. It must be a 12-byte input or a 24-character hex string'

    @staticmethod
    def no_file_uploaded():
        return 'No file is uploaded.'

    @staticmethod
    def admin_permission_required():
        return 'Admin permission is required.'
