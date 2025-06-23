from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# https://www.gradescope.com/courses/934968/assignments/6046743/review_grades
 

"""Create files from gradescope"""

def extract_student_assingments(assignemnt_numbers_list: list[str], course_number: int, location: str, files_wanted: list[str] = None):
    driver = webdriver.Chrome()

    for assingemnt in assignemnt_numbers_list:
        driver.get(f"https://www.gradescope.com/courses/{course_number}/assignments/{assingemnt}/review_grades")


        # Find the search box, type a query, and press Enter
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium Python")
        search_box.send_keys(Keys.RETURN)

        # Wait a few seconds to see results
        time.sleep(3)

        # Close the browser
        driver.quit()