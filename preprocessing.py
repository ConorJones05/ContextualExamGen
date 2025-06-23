import ast
import os 
import regex as re


"""Step to cleaning the code for use within assingment."""


def create_dict_code(source_code_folder: str, language: str):
    """Finds students names, pid, and appends finished preprocessing code to dictionary"""
    file_names = os.scandir(source_code_folder)
    if file_names is None:
        ValueError("No files found: aborting process.")
    print("Loading Student folders")
    student_dict = {"name": [], "pid": [], "code": []}

    # Student name and PID
    for student_folder in file_names:
        match = re.match(r'^([a-zA-Z]+)_([0-9]+)_', student_folder)
        if match:
            student_dict['name'].append(match.group(1))
            student_dict['name'].append(match.group(2))

        raw_code = load_code(student_code_folder=student_folder)
        raw_code = strip_comments_and_docstrings(language)
        cleaned_code = remove_long_strings_and_lists(language, raw_code)
        student_dict['code'].append(cleaned_code)



# TODO fix this to work with the new process files code
def load_code(student_code_folder: str):

    file_names = os.scandir(student_code_folder)
    if file_names is not None:
        print(f"Acessed files in {student_code_folder}")
    else: 
        print(f"{student_code_folder} contains incorrect or no folders")
        exit
    
    code_text = ""
    
    for _ in file_names:
        with open(file_names, "r", encoding="utf-8") as f:
            code_text += f.read()

def strip_comments_and_docstrings(language: str, code: str):
    if language == "python":
        code = re.sub(r'("""|\'\'\')(.*?)(\1)', '', code, flags=re.DOTALL)
        code = re.sub(r'#.*', '', code)
        code = re.sub("\n\n", "\n", code)
        return code
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
    code = re.sub(r'".{20,}"', '"<omitted long string>"', code)
    code = re.sub(r'\[.*?\]', '[...]', code)

#  TODO add shorter getter setter methods     



