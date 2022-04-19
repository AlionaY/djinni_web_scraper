import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def open_jobs_list(login, password, job, social_auth_type):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    website = 'https://djinni.co/my/dashboard/'
    driver.get(website)

    social = "//button[@value='" + social_auth_type + "']"
    driver.find_element(By.XPATH, social).click()
    driver.find_element(By.ID, "username").send_keys(login)
    driver.find_element(By.ID, "password").send_keys(password)
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[@aria-label='Sign in']").click()
    nav_bar_collapse = driver.find_element(By.XPATH, "//div[@class='collapse navbar-collapse']")
    nav_bar = nav_bar_collapse.find_element(By.XPATH, "//ul[@class='nav navbar-nav']")
    nav_bar.find_element(By.XPATH, "./li[2]").click()
    time.sleep(2)

    job_name = "//a[@href='/jobs/keyword-" + job + "/']"
    driver.find_element(By.XPATH, job_name).click()

    job_header = []
    job_description = []
    company_location = []
    company_type = []

    job_items = driver.find_elements(By.XPATH, '//div[@class="list-jobs__title"]')
    driver.quit()
