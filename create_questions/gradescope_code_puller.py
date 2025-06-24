"""Create folders containing folders that hold raw student code."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 

def create_all_files(course_number: int, assignemnt_numbers_list,files_wanted, path, folder_name):
    """The mainfunction creates folders and subfolders that contain the students raw code.

    Parameters
    ----------
    course_number : int
        The number of reffrence on Gradescope found www.gradescope.com/courses/_________
    
    """

    # Driver settup and gradescope auth process
    driver = webdriver.Chrome()
    driver.get(f"https://www.gradescope.com/courses/{course_number}")
    input("=======================================================\n Please press ENTER when you have logged into Gradescope.\n=======================================================")
    print("STARTING GENERATION")
    student_dict = extract_student_assingments_dict(driver,assignemnt_numbers_list, course_number,files_wanted)
    create_folders(student_dict, path, folder_name)
    print(student_dict.keys(), student_dict)
    

    


def scrape_one_assingemnt(driver, course_number: int, assingemnt: int) -> tuple[list[str], list[str], list[str]]:
    driver.get(f"https://www.gradescope.com/courses/{course_number}/assignments/{assingemnt}/review_grades")
    print(f"Connecting to https://www.gradescope.com/courses/{course_number}/assignments/{assingemnt}/review_grades")
    email_list = []
    name_list = []
    assingements_link_list = []

    emails = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
    for email in emails:
        email_link = email.get_attribute("href")
        email_address = email_link.replace("mailto:", "")
        email_list.append(email_address)
        
    linked_names = driver.find_elements(By.CLASS_NAME, "link-gray")
    for names in linked_names:
        name = names.text
        name_list.append(name)
        
        link = names.get_attribute("href")
        assingements_link_list.append(link)
    print("All linked items selected")

    unlinked_names = driver.find_elements(By.CLASS_NAME, "sorting_3")
    for names in unlinked_names:
        name = names.text
        name_list.append(name)
        assingements_link_list.append(None)
    print("All unlinked items selected")
    return name_list, email_list, assingements_link_list


def extract_student_assingments_dict(driver, assignemnt_numbers_list: list[str], course_number: int, files_wanted: list[str] = None):
    name_list, email_list, assignments_link_list = scrape_one_assingemnt(driver, course_number, assignemnt_numbers_list[0])
    
    name_by_email = dict(zip(email_list, name_list))
    assignment_by_email = dict(zip(email_list, assignments_link_list))

    data = {}

    for email in email_list:
        data[email] = {
            "name": name_by_email.get(email),
            "assignment": assignment_by_email.get(email)
        }
    
    if len(assignemnt_numbers_list) > 1:
        for assignment in assignemnt_numbers_list[1:]:
            name_list, email_list, assignments_link_list = scrape_one_assingemnt(driver, course_number, assignment)
            for email in email_list:
                data[email] = {
                    "name": name_by_email.get(email),
                    "assignment": assignment_by_email.get(email)
            }
    return data


def create_folders(student_dict: dict, path: str, folder_name: str) -> None:
    """Creates empty base fodler and all subfolders"""
    try:
        os.mkdir(f"{path}/{folder_name}")
        os.chdir(f"{path}/{folder_name}")
        for email in student_dict.keys():
            os.mkdir(f"{email}_{student_dict['name']}")
        print("Folders created sucessfully!")
    except Exception:
        print("Error in creating your folders.")
    

def download_raw_code_files(driver, link: str):
    print(f"Starting download for {link}")
    try:
        driver.get(f"{link}?view=files")
    except Exception:
        print(f"Error acessing {link}")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.standaloneLink.link.link-gray.fileViewerHeader--downloadLink"))
        )
        aws_download_links = driver.find_elements(By.CSS_SELECTOR, "a.standaloneLink.link.link-gray.fileViewerHeader--downloadLink")

        if not aws_download_links:
            print("No download links found.")
        else:
            for file in aws_download_links:
                file_link = file.get_attribute("href")
                driver.get(file_link)
                print(f"File: {file_link} downloaded")

    except Exception as e:
        print("Error while trying to extract download links:", e)