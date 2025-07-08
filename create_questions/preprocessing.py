import ast
import os 
import regex as re
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from tools import write_to_file

load_dotenv()
fernet_key = os.getenv("FERNET_KEY")



def encript_student_name(file_name: str):
    f = Fernet(fernet_key.encode())
    encrypted_name = f.encrypt(file_name.encode())
    return encrypted_name

# decrypted = f.decrypt(encrypted).decode()
#     print(f"Decrypted: {decrypted}")

# def create_dict_code(source_code_folder: str, language: str):
#     """Finds students names, pid, and appends raw links to assignemnts to the dict"""
#     file_names = os.scandir(source_code_folder)
#     if file_names is None:
#         ValueError("No files found: aborting process.")
#     print("Loading Student folders")
#     student_dict = {"name": [], "email": [], "code": []}

#     # Student name and PID
#     for student_folder in file_names:
#         match = re.match(r'^([a-zA-Z]+)_([a-zA-Z]+)_', student_folder)
#         if match:
#             student_dict['name'].append(match.group(1))
#             student_dict['name'].append(match.group(2))

#         raw_code = load_code(student_code_folder=student_folder)
#         raw_code = strip_comments_and_docstrings(language)
#         cleaned_code = remove_long_strings_and_lists(language, raw_code)
#         student_dict['code'].append(cleaned_code)


def load_code(student_code_folder: str):
    file_names = os.scandir(student_code_folder)
    names = []
    for file_name in file_names:
        names.append(file_name.name)
    if file_names is not []:
        print(f"Acessed files in {student_code_folder}")
    else: 
        print(f"{student_code_folder} contains incorrect or no folders")
        exit
    
    code_text = ""
    for file in names:
        with open(f"{student_code_folder}/{file}", "r", encoding="utf-8") as f:
            code_text += f.read()
    return code_text



def strip_comments_and_docstrings(language: str, code: str):
    if language == "python":
        code = re.sub(r'("""|\'\'\')(.*?)(\1)', '', code, flags=re.DOTALL)
        code = re.sub(r'#.*', '', code)
        code = re.sub("\n\n", "\n", code)
    elif language == "java":
        code = re.sub(r'(/*)(.*?)(\1)', '', code, flags=re.DOTALL)
        code = re.sub(r'//.*', '', code)
        code = re.sub("\n\n", "\n", code)
    return code


def list_fucntions(language: str, code: str):
    if language == 'python':
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return functions
    
def remove_long_strings_and_lists(language: str, code: str):
    code = re.sub(r'".{20,}"', '"<long string>"', code)
    code = re.sub(r'\[.*?\]', '[...]', code)
    return code



def preprocess_data(language: str, path: str):
    folder_names = os.scandir(path)
    folders = []
    for folder_name in folder_names:
        folders.append(folder_name.name)    
    os.mkdir(f"{path}/preprocessed_files")
    print("============================\nMade Preprocessed Folder\n============================")
    
    for folder in folders:
        raw_text = load_code(f"{path}/{folder}")
        stripped_text = strip_comments_and_docstrings(language, raw_text)
        shorten_text = remove_long_strings_and_lists(language, stripped_text)
        file_name = encript_student_name(folder)
        write_to_file(f"{path}/preprocessed_files/{file_name}", shorten_text)
        write_to_file(f"{path}/{folder}/{file_name}", shorten_text)
    print("============================\nFinished Processing data\n============================")


preprocess_data("python", r"C:\Users\conor\LLM_Question_Gen\test_files\data\testing")


#  TODO add shorter getter setter methods     

# print(remove_long_strings_and_lists("python",strip_comments_and_docstrings("python",load_code(r"C:\Users\conor\LLM_Question_Gen\test_files\data\step_one_scrape\ihinks@cs.edu_Izzi Hinks"))))

