import os


def delete_file(filename):
    try:
        os.remove(filename)
    except OSError as e:
        print(e)


def rename_file(old, new):
    try:
        os.rename(old, new)
    except OSError as e:
        print(e)


def get_file_extension(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return file_extension


def get_file_name(file_path):
    filename, file_extension = os.path.splitext(file_path)
    return filename


def get_filename_from_url(url):
    return os.path.basename(url)
