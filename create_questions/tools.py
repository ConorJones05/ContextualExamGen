def write_to_file(full_path, text):
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(text)

def read_file(full_path):
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()