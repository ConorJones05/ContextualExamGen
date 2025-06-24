from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# https://www.gradescope.com/courses/934968/assignments/6046743/review_grades
 

"""Create files from gradescope"""
def create_all_folders(course_number: int):
    driver = webdriver.Chrome()
    driver.get(f"https://www.gradescope.com/courses/{course_number}")
    input("=======================================================\n Please Press ENTER when you have logged into Gradescope.\n=======================================================")




def extract_student_assingments_dict(driver, assignemnt_numbers_list: list[str], course_number: int, location: str, files_wanted: list[str] = None):
    student_assn_dict = {"name":[], "email":[], "assignment_list":[]}


    for assingemnt in assignemnt_numbers_list:
        driver.get(f"https://www.gradescope.com/courses/{course_number}/assignments/{assingemnt}/review_grades")
        print(f"Connecting to https://www.gradescope.com/courses/{course_number}/assignments/{assingemnt}/review_grades")

        emails = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
        for email in emails:
            email_link = email.get_attribute("href")
            email_address = email_link.replace("mailto:", "")
            if email_address not in student_assn_dict["email"]:
                student_assn_dict["email"].append(email_address)
            
        linked_names = driver.find_elements(By.CLASS_NAME, "link-gray")
        for names in linked_names:
            name = names.text
            if name not in student_assn_dict["name"]:
                student_assn_dict["name"].append(name)
            link = names.get_attribute("href")
            link_list = []
            # TODO: fix this

            link_list.append(link)
            student_assn_dict['assignment_list'].append(link_list)
        print("All linked items selected")

        unlinked_names = driver.find_elements(By.CLASS_NAME, "sorting_3")
        for names in unlinked_names:
            name = names.text
            if name not in student_assn_dict["name"]:
                student_assn_dict["name"].append(name)
        print("All unlinked items selected")
    driver.quit()
    return student_assn_dict

# extract_student_assingments_dict([6037940, 6089439], 934968, "")


def create_folders(student_dict: dict, path: str, name: str):
    os.mkdir(f"path/{name}", exist_ok = False)
    os.chdir(f"path/{name}")
    for email in student_dict['email']:
        os.mkdir(f"{email}_{student_dict['name']}", exist_ok = True)
        download_links(driver=driver)

def download_links(driver, link):
    print("download files")
    driver.get(f"{link}?view=files")
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
        

driver = webdriver.Chrome()
driver.get(f"https://www.gradescope.com/courses/{934968}")
input("=======================================================\n Please Press ENTER when you have logged into Gradescope.\n=======================================================")
download_links(driver,"https://www.gradescope.com/courses/934968/assignments/5843165/submissions/311553334")
driver.quit()