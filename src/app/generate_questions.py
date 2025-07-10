"""Script in charge of creating questions. Scrapes student code, Preprocesses it, sends to batch infrence model"""

from create_questions.gradescope_code_puller import create_all_files
from create_questions.preprocessing import preprocess_data
from create_questions.query_manufacturing import create_batch_job 

def main(course_number: int, assignemnt_numbers_list: list[int], path: str, folder_name: str, files_wanted: list[str] = None):
    create_all_files()
    preprocess_data()
    create_batch_job()
    

