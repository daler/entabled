import os


def data_dir():
    return os.path.join(os.path.dirname(__file__), 'data')


def data_file(fn):
    result = os.path.join(data_dir(), fn)
    if not os.path.exists(result):
        raise ValueError("File %s does not exist" % fn)
    return result
