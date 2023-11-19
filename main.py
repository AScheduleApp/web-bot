import hashlib
import json
import os
from datetime import datetime

import requests
from selenium.webdriver.common.by import By

from bot import WebBot

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("PASSWORD")
PATH_SAVE_FILES = os.getenv(
    "PATH_SAVE_FILES", "/home/michal/workspaces/AScheduleApp/web-bot/media_files"
)
THRESHOLD_TIME_MIN = int(os.getenv("THRESHOLD_TIME", 5)) * 60

if __name__ == "__main__":
    options = {
        "download.default_directory": PATH_SAVE_FILES,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    bot = WebBot(
        options=[
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ],
        experimental_options=options,
    )

    print(f"Start bot at {datetime.now()} \n")

    bot.open_page(
        url="https://auth-dziekanat.wst.com.pl/Account/Login?ReturnUrl=%2F",
        time_sleep_sec=2,
    )

    bot.click_button(
        by=By.CLASS_NAME, value="social-media", time_sleep_sec=2
    )  # Redirect to login page

    bot.add_input(by=By.ID, value="i0116", text=EMAIL_ADDRESS)  # Enter e-mail
    bot.click_button(
        by=By.ID, value="idSIButton9", time_sleep_sec=2
    )  # Click and redirect to enter password

    bot.add_input(by=By.ID, value="i0118", text=PASSWORD)  # Enter password
    bot.click_button(
        by=By.ID, value="idSIButton9", time_sleep_sec=3
    )  # Redirect to YES or NO modal

    print("Logged.")

    bot.click_button(
        by=By.ID, value="idSIButton9", time_sleep_sec=4
    )  # Redirect to nDziekenat

    bot.click_button(
        by=By.CLASS_NAME, value="btn-primary", time_sleep_sec=6
    )  # Click "Return to nDziekanat"

    bot.open_page(
        url="https://dziekanat.wst.com.pl/pl/repozytorium-plikow", time_sleep_sec=5
    )  # Open page

    bot.add_input(by=By.ID, value="nazwa-input", text="lekarski semestr 3")
    bot.click_button(by=By.XPATH, value='//button[text()="Szukaj"]', time_sleep_sec=1)

    bot.click_button(
        by=By.XPATH,
        value='//button[contains(text(), "Lekarski semestr 3")]',
        time_sleep_sec=5,
    )
    print("Saved file.")

    bot.close_page()

    file = open("/app/mediafiles/Lekarski semestr 3.xls", "rb")
    file_binary_content = file.read()
    md5_file = hashlib.md5(file_binary_content).hexdigest()
    print(f"MD5: {md5_file}")
    print("Sent file to API.")
    file.seek(0)
    files = {"file": file}
    requests.post("http://fastapi_app:8000/schedule", files=files)
    file.close()
    os.remove("/app/mediafiles/Lekarski semestr 3.xls")
    print(f"Finish bot at {datetime.now()} \n")
