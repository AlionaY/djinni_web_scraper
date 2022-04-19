import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager


def find_elem(row, elem):
    return row.find_element(By.XPATH, elem).text


def export_football_data():
    website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website)
    # allocate an element width selenium
    # label is tag name
    # analytics-event is attribute name
    # find tag name and attribute name you can from site (right-handed click - inspect)
    all_matches_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
    all_matches_button.click()
    try:
        dropdown = Select(driver.find_element(By.ID, "country"))
        dropdown.select_by_visible_text("Spain")
        time.sleep(3)

        # rows
        matches = driver.find_elements(By.TAG_NAME, 'tr')

        date = []
        home_team = []
        score = []
        away_team = []

        for match in matches:
            # '.' means than there is/are block(s) (tr) before the current block
            date.append(find_elem(match, "./td[1]"))
            home = find_elem(match, "./td[2]")
            home_team.append(home)
            print(home)
            score.append(find_elem(match, "./td[3]"))
            away_team.append(find_elem(match, "./td[4]"))
    except Exception as err:
        print(err)

        driver.quit()

        df = pd.DataFrame({
            'date': date,
            'home_team': home_team,
            'score': score,
            'away_team': away_team
        })

        df.to_csv('C:/Users/Home/Desktop/ds/football_data.csv', index=False)