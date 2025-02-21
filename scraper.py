from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # NOQA
from dotenv import dotenv_values
import time

CONFIG = dotenv_values()


def scrape_data():
    stats = {}

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

        popup_container = driver.find_element(By.ID, "popupsContainer")
        if popup_container:
            driver.execute_script("""
                        var popupContainer = document.getElementById('popupsContainer');
                        if (popupContainer) {
                            popupContainer.innerHTML = '';
                        }
                    """)

        elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'v-popover') and contains(@class, 'uber_game_tile') and contains(@class, 'button_click')]"
        )

        def get_data():
            driver.switch_to.default_content()
            iframe = WebDriverWait(driver, 20).until(  # NOQA
                EC.presence_of_element_located((By.ID, "ifm"))
            )
            driver.switch_to.frame(iframe)

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

            driver.execute_script("document.elementFromPoint(1, 1).click();")

            return_to_menu = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "#func_miniprofile_cont > div.actions.row > div.func_button_home.con_button.mini_profile_topbutton"
                ))
            )
            return_to_menu.click()

        count = len(elements)
        for x in range(1, count + 1):
            if x != 1:
                driver.switch_to.default_content()
                ifr = driver.find_element(By.ID, "ifm")
                driver.switch_to.frame(ifr)

                driver.execute_script("""
                                       var popupContainer = document.getElementById('popupsContainer');
                                       if (popupContainer) {
                                           popupContainer.innerHTML = '';
                                       }
                                   """)

            enter_game = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f"#uber_my_games > div:nth-child({x}) > div > div"))
            )
            enter_game.click()
            get_data()

            time.sleep(3)  # TODO: not sure how many to be

        # print(stats)
        # time.sleep(100)
    finally:
        driver.quit()

    return stats
