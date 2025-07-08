"""Create folders containing folders that hold raw student code."""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time




def create_all_files(course_number: int, assignemnt_numbers_list: list[int], path, folder_name: str, files_wanted: list[str] = None):
    """The mainfunction creates folders and subfolders that contain the students raw code.

    Parameters
    ----------
    course_number : int
        The number of reffrence on Gradescope found www.gradescope.com/courses/_________
    
    """

    # Driver settup and gradescope auth process
    start_time = time.time()
    driver = webdriver.Chrome()
    driver.get(f"https://www.gradescope.com/courses/{course_number}")
    input("=======================================================\n Please press ENTER when you have logged into Gradescope.\n=======================================================")
    print("STARTING GENERATION")
    try:
        student_dict = extract_student_assingments_dict(driver,assignemnt_numbers_list, course_number, files_wanted)
        print("Scraped all student data.")
        print(student_dict)
    except Exception as e:
        print("Failed to scrape student data", e)
        exit

    try:
        create_folders(student_dict, path, folder_name)
        print(f"Created all blank files at {path} named {folder_name}")
    except Exception as e:
        print(f"Error creating blank files at {path} named {folder_name}", e)
        exit()
        #  TODO if failure remove old files

    os.chdir(f"{path}/{folder_name}")
    for i, email in enumerate(student_dict.keys()):
        current_dict = f"{path}/{folder_name}/{email}_{student_dict[email]['name']}"
        for link in student_dict[email]['assignment']:
            download_raw_code_files(driver=driver, link=link, file_path=current_dict)

        print(f"{100 * (i/len(student_dict.keys())):.2f}% complete")
    
    print(f"--- Process took {((time.time() - start_time) / 60):.2f} minutes ---")
    
    


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
            "assignment": [assignment_by_email.get(email)]
        }
    #  TODO: Fix this logic to append the new links
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
        os.mkdir(f"{path}/{folder_name}", mode=644)
        os.chdir(f"{path}/{folder_name}")
        for email in student_dict.keys():
            os.mkdir(f"{email}_{student_dict[email]['name']}", mode=644)
            print(f"Created file: {email}_{student_dict[email]['name']}")
        print("Folders created sucessfully!")
    except Exception as e:
        print("Error in creating your folders.", e)




def download_raw_code_files(driver, link: str, file_path: str):
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
                response = requests.get(file_link)
                if response.status_code == 200:
                    filename = file_link.split("/")[-1].split("?")[0]
                    full_path = os.path.join(file_path, filename)
                    text = response.content.decode('utf-8')

                    os.makedirs(file_path, exist_ok=True, mode=644)

                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(text)

    except Exception as e:
        print("Error while trying to extract download links:", e)

create_all_files(934968, [5843165], r"c:\Users\conor\Downloads", "testing")

# mock_student_dict = {"conor@gmail.com": {'name': "conor", 'assignment': "Hello"}, "sdf@gmail.com": {'name': "sdf", 'assignment': "Hello"}, "asdfsdf@gmail.com": {'name': "asdfaff", 'assignment': "Hello"}}

# create_folders(mock_student_dict, r"c:\Users\conor\Downloads", "testing")