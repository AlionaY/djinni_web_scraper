import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# collect all job links on each web page
# open each job description from list (above)


def open_jobs_list(login, password, job, social_auth_type):
    website = 'https://djinni.co/my/dashboard/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website)

    login_to_djinni(driver, login, password, social_auth_type)
    open_job_list(driver, job)

    job_header = []
    job_description = []
    company_location = []
    company_type = []

    wait = WebDriverWait(driver, 5)
    time.sleep(3)

    xpath = '//ul[@class="pagination pagination_with_numbers"]//li[last()]//a[not(@aria-disabled)]'

    while True:
        try:
            next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            next_page_button.click()
            add_jobs_to_list(driver, job_header)
            time.sleep(2)
            print("header", len(job_header))
        except Exception as err:
            print(err)
            break

    df = pd.DataFrame(job_header, columns=["job_header"])
    print(df.to_markdown())


def add_jobs_to_list(driver, job_header):
    job_items = driver.find_elements(By.CLASS_NAME, "profile")
    for item in job_items:
        job_header.append(item.text)
    time.sleep(2)


def open_job_list(driver, job):
    nav_bar_collapse = driver.find_element(By.XPATH, "//div[@class='collapse navbar-collapse']")
    nav_bar = nav_bar_collapse.find_element(By.XPATH, "//ul[@class='nav navbar-nav']")
    nav_bar.find_element(By.XPATH, "./li[2]").click()
    time.sleep(2)
    job_name = "//a[@href='/jobs/keyword-" + job + "/']"
    driver.find_element(By.XPATH, job_name).click()


def login_to_djinni(driver, login, password, social_auth_type):
    social = "//button[@value='" + social_auth_type + "']"
    driver.find_element(By.XPATH, social).click()
    driver.find_element(By.ID, "username").send_keys(login)
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@aria-label='Sign in']").click()