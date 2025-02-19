from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import dotenv_values
import os
import time

CONFIG = dotenv_values()


def scrape_data():
    username = CONFIG['USERNAME']
    password = CONFIG['PASSWORD']

    driver_path = "./chromedriver-win64/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://www.conflictnations.com/")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tab")))

        login_button = driver.find_element(By.CSS_SELECTOR, "div.tab[data-form='login']")
        login_button.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "user"))
        )

        username_field = driver.find_element(By.NAME, "user")
        password_field = driver.find_element(By.NAME, "pass")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(5)

        iframe = driver.find_element(By.ID, "ifm")
        driver.switch_to.frame(iframe)

        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "popupsContainer"))
            )
        except TimeoutException:
            pass

        popup_container = driver.find_element(By.ID, "popupsContainer")
        if popup_container:
            driver.execute_script("""
                        var popupContainer = document.getElementById('popupsContainer');
                        if (popupContainer) {
                            popupContainer.innerHTML = '';
                        }
                    """)

        enter_game = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#uber_my_games > div:nth-child(1) > div > div"))
        )
        enter_game.click()

        # time.sleep(10)

        driver.switch_to.default_content()

        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "ifm"))
        )
        driver.switch_to.frame(iframe)

        stats = {}
        nation = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#func_miniprofile_cont > div.miniprofile_name_container.func_open_profile_tooltip > div > "
                "div:nth-child(2)"))
        ).text
        stats[nation] = []

        diplomacy = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "func_btn_newspaper"))
        )
        diplomacy.click()

        victory_points = []
        while True:
            time.sleep(0.2)

            ranking_points_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "#newspaper_ranking_single > div.viewport > div > ol > li.is_self > div.ranking_points"))
            )

            inner_html = int(ranking_points_element.get_attribute("innerText").strip())

            victory_points.append(inner_html)
            button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#func_day_down"))
            )
            button.click()

            current_day_element = driver.find_element(By.CSS_SELECTOR, "#func_newspaper_day_tf")
            current_day_value = current_day_element.get_attribute("value")

            if current_day_value == "1":
                break

        victory_points.reverse()
        stats[nation].extend(victory_points)
        # print(stats)
        # time.sleep(100)
    finally:
        driver.quit()

    return stats
