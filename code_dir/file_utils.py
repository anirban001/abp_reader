
def read_file(file_path):
    with open(file_path, 'r') as fp:
        return fp.read()


def write_file(file_path, file_text):
    with open(file_path, 'w') as fp:
        fp.write(file_text)
