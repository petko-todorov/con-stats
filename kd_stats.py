import matplotlib.pyplot as plt
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # NOQA
from selenium.webdriver.chrome.options import Options
from dotenv import dotenv_values
from tabulate import tabulate

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "kd_stats.csv")

CONFIG = dotenv_values()


def scrape_kd_stats():
    username = CONFIG['USERNAME']
    password = CONFIG['PASSWORD']

    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "Pixel 2"})

    driver_path = "./chromedriver-win64/chromedriver.exe"
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.conflictnations.com/")

        existing_account_btn = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "func_sg_loginform_button"))
        )
        existing_account_btn.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "user"))
        )

        username_field = driver.find_element(By.NAME, "user")
        password_field = driver.find_element(By.NAME, "pass")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(3)

        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
        )

        try:
            first_play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "#uber_menu_game_list_container > div.uber_menu_games_list > ul > li:nth-child(1) > div.content > "
                    "div > div > span"
                ))
            )
            first_play_button.click()
        except:  # NOQA
            print("button not found")

        time.sleep(2)

        driver.execute_script("document.elementFromPoint(1, 1).click();")

        window_width = driver.execute_script("return window.innerWidth")
        window_height = driver.execute_script("return window.innerHeight")

        center_x = window_width / 2
        center_y = window_height / 2

        actions = ActionChains(driver)
        actions.move_by_offset(center_x, center_y - 50).click().perform()

        # TODO: enable
        # time.sleep(1)

        try:
            WebDriverWait(driver, 1).until(
                EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
            )
        except:  # NOQA
            pass

        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     "#mapSelector > ul > li.province_element.selector_element > div")
                )
            ).click()
            # print("Country image found")
        except:  # NOQA
            pass

        # TODO: enable
        time.sleep(1)
        try:
            country = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#province_bar > div > header > div.bar_header.top > div.hup_player_flag > span > img"
                    ))
            )
        except:  # NOQA
            country = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#army_bar > div.hup_top_bar > header > div.bar_header.top > div.hup_player_flag > span > img"
                    ))
            )

        img_src = country.get_attribute("src")
        img_name = img_src.split("/")[-1].split(".")[0].split("_")[1].upper()
        country.click()

        player_list_container = driver.find_element(By.CSS_SELECTOR, "#player_list")

        def scroll_and_find_country():
            last_height = driver.execute_script("return arguments[0].scrollHeight", player_list_container)

            while True:
                flag_images = driver.find_elements(By.CSS_SELECTOR,
                                                   "#player_list .vue-recycle-scroller__item-view .hup_player_flag img")
                for flag in flag_images:
                    img_src = flag.get_attribute("src")
                    img_name_in_list = img_src.split("/")[-1].split(".")[0].split("_")[1].upper()

                    if img_name_in_list == img_name:
                        profile_entry = flag.find_element(By.XPATH, "../../..")
                        profile_entry.click()
                        return

                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", player_list_container)

                new_height = driver.execute_script("return arguments[0].scrollHeight", player_list_container)
                if new_height == last_height:
                    break
                last_height = new_height

        time.sleep(1)
        scroll_and_find_country()

        profile_stats = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#playerDetailContainer > div > div.hup_fullscreen_widget > main > div > section > "
                 "div.player_actions_container > div > div:nth-child(2) > div > span")
            )
        )
        profile_stats.click()

        kills_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_statistics_graph > "
                 "div.graph_bar_entries > div:nth-child(1) > div.graph_value"
                 )
            ))

        kills_stat_vs_players = kills_stat_element.text

        deaths_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_statistics_graph > "
                 "div.graph_bar_entries > div:nth-child(2) > div.graph_value"
                 )
            )
        )
        deaths_stat_vs_players = deaths_stat_element.text

        kd_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_kill_death_ratio_container > "
                 "div.unit_kill_death_ratio_value"
                 )
            ))
        kd_stat_vs_players = kd_stat_element.text

        profile_stats = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.icon_label_container.toggle_stats_button"
                 )
            )
        )
        profile_stats.click()

        kills_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_statistics_graph > "
                 "div.graph_bar_entries > div:nth-child(1) > div.graph_value"
                 )
            ))

        kills_stat_vs_ai = kills_stat_element.text

        deaths_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_statistics_graph > "
                 "div.graph_bar_entries > div:nth-child(2) > div.graph_value"
                 )
            )
        )
        deaths_stat_vs_ai = deaths_stat_element.text

        kd_stat_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 "#user_profile_game_stats > div > div > div.unit_and_province_statistics > "
                 "div.unit_statistics_container > div.unit_statistics > div.unit_kill_death_ratio_container > "
                 "div.unit_kill_death_ratio_value"
                 )
            ))
        kd_stat_vs_ai = kd_stat_element.text

        # print(kills_stat_vs_players, deaths_stat_vs_players, kd_stat_vs_players)
        # print(kills_stat_vs_ai, deaths_stat_vs_ai, kd_stat_vs_ai)

        kd_data = {
            'new': [
                int(kills_stat_vs_players),
                int(deaths_stat_vs_players),
                float(kd_stat_vs_players),
                int(kills_stat_vs_ai),
                int(deaths_stat_vs_ai),
                float(kd_stat_vs_ai)
            ]
        }

    finally:
        driver.quit()

    return kd_data


def save_kd_stats_to_csv(kd_stats):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if os.path.exists(CSV_FILE) and os.stat(CSV_FILE).st_size > 0:
        existing_df = pd.read_csv(CSV_FILE)

        previous_new = existing_df[existing_df["Type"] == "New"]

        existing_df = existing_df[~existing_df["Type"].isin(["Old", "New"])]

        if not previous_new.empty:
            previous_new["Type"] = "Old"
            existing_df = pd.concat([existing_df, previous_new], ignore_index=True)

    else:
        existing_df = pd.DataFrame()

    new_df = pd.DataFrame([["New"] + kd_stats["new"]],
                          columns=["Type", "Kills vs Players", "Deaths vs Players", "K/D vs Players",
                                   "Kills vs AI", "Deaths vs AI", "K/D vs AI"])

    updated_df = pd.concat([existing_df, new_df], ignore_index=True)

    updated_df.to_csv(CSV_FILE, index=False)


def visualize_kd_stats():
    try:
        df = pd.read_csv(CSV_FILE)
        categories = ['K/D vs Players', 'K/D vs AI']
        print(tabulate(df, headers='keys', tablefmt='rounded_outline', numalign="center", stralign="center",
                       showindex="never"))

        try:
            old_values = df[df['Type'] == 'Old'][categories].iloc[0].tolist()
        except:  # NOQA
            print("No 'Old' data found in the CSV file.")
            old_values = [0] * len(categories)

        new_values = df[df['Type'] == 'New'][categories].iloc[0].tolist()

        x = range(len(categories))
        width = 0.3

        fig, ax = plt.subplots(figsize=(9, 6))

        max_value = max(max(old_values), max(new_values))
        ax.set_ylim(0, max_value + 1)

        for i, category in enumerate(categories):
            old_value = old_values[i]
            new_value = new_values[i]

            if old_value == new_value:
                old_value_str = str(f"{old_value:.2f}")
                ax.bar(i, old_value, width * 1.5, color='#006600', edgecolor='black',
                       label='Same K/D' if i == 0 else "")
                # ax.text(i, old_value + 0.05, str(round(old_value, 2)), ha='center', va='bottom', fontsize=12)
                ax.text(i, old_value + 0.05, old_value_str, ha='center', va='bottom', fontsize=12)
                ax.text(i, old_value + 0.5, "Old and New K/D are the same",
                        ha='center', va='bottom', fontsize=12, clip_on=True)
            else:
                old_value_str = str(f"{old_value:.2f}")
                new_value_str = str(f"{new_value:.2f}")
                ax.bar(i - width / 2, old_value, width, color='gray', edgecolor='black',
                       label='Old K/D' if i == 0 else "")
                ax.bar(i + width / 2, new_value, width, color='skyblue', edgecolor='black',
                       label='New K/D' if i == 0 else "")
                ax.text(i - width / 2, old_value + 0.05, old_value_str, ha='center', va='bottom',
                        fontsize=12)
                ax.text(i + width / 2, new_value + 0.05, new_value_str, ha='center', va='bottom', fontsize=12)

        ax.set_ylabel("K/D Ratio")
        ax.set_title("Comparison of K/D vs Players and K/D vs AI")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45)
        ax.legend()

        plt.tight_layout()
        plt.show()
    except:  # NOQA
        print("No data found. Please scrape data first.")
