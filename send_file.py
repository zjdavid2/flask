from flask import send_from_directory


def send_file_from_directory(directory, file_name):
    return send_from_directory(directory, file_name)
