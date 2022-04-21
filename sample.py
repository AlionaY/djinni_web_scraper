import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# collect all job links on each web page
# open each job description from list (above)


def save_job_data(login, password, job, social_auth_type):
    website = 'https://djinni.co/my/dashboard/'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website)
    wait = WebDriverWait(driver, 5)

    login_to_djinni(driver, wait, login, password, social_auth_type)
    open_job_list(wait, job)

    job_header = []
    job_description = []
    company_location = []
    company_type = []
    job_links = []

    time.sleep(3)

    xpath = '//ul[@class="pagination pagination_with_numbers"]//li[last()]//a[not(@aria-disabled)]'

    while True:
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            save_job_link(driver, job_links)
            time.sleep(2)
        except Exception as err:
            print(err)
            break

    save_data_to_scv(company_location, company_type, driver, job, job_description, job_header, job_links)


def save_data_to_scv(company_location, company_type, driver, job, job_description, job_header, job_links):
    for job_name in job_links:
        try:
            driver.get(job_name)
            job_header.append(driver.find_element(By.XPATH, '//div[@class="job-post--title-wrapper"]//h1').text)
            job_description.append(driver.find_element(By.CLASS_NAME, "profile-page-section").text)
            company_location.append(driver.find_element(By.CLASS_NAME, "inbox-candidate-details--item-text").text)
            company_type.append(driver.find_element(By.CLASS_NAME, "inbox-candidate-details--item-inner").text)
            print(driver.find_element(By.XPATH, '//div[@class="job-post--title-wrapper"]//h1').text)
        except Exception as err:
            print(err)

    columns = ['job_header', 'description', 'location', 'company_type']
    df = pd.DataFrame(list(zip(job_header, job_description, company_location, company_type)), columns=columns)
    # print(df.to_markdown())
    path = 'C:/Users/Home/Desktop/ds/djinni_' + job + '_data.csv'
    df.to_csv(path, index=True)


def save_job_link(driver, job_links):
    job_list = driver.find_elements(By.XPATH, '//div[@class="list-jobs__title"]//a[@class="profile"]')
    for job in job_list:
        print(job.get_attribute('href'))
        job_links.append(job.get_attribute('href'))
    time.sleep(1)


def open_job_list(wait, job):
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='collapse navbar-collapse']")))
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='collapse navbar-collapse']//ul[@class='nav "
                                                     "navbar-nav']//li[2]"))).click()
    job_name = "//a[@href='/jobs/keyword-" + job + "/']"
    wait.until(EC.element_to_be_clickable((By.XPATH, job_name))).click()


def login_to_djinni(driver, wait, login, password, social_auth_type):
    social = "//button[@value='" + social_auth_type + "']"
    wait.until(EC.element_to_be_clickable((By.XPATH, social))).click()
    driver.find_element(By.ID, "username").send_keys(login)
    driver.find_element(By.ID, "password").send_keys(password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Sign in']"))).click()