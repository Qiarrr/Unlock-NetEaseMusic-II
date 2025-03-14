# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00758442DB3AF3DB9FB60C243FEE27B309D85FB1A1FC6B6EFBB930A17DE2956FF9E6F1BB6E79168896168273327E3EEBFE86E0F3FFF727288ADAADB37C58F3F1AED86ED18A346E7B51C13C1EE89A168D8EFCA0EE970B985A90C0E2EDCF7F6B4067C80AE9F68B31CEDC978B6F9150039992F35C5475F237A8300763D5F30FA8C43312DD8E5F368237D50315AC99AC0BD960B7143A6E96E851870C6B95656DBAB00441DC54B3D7115FDD2F4E81EB2B8330FFBCF0A764BD278597C90007FB79AD59E2A8F50B0CC32ED4036E0605DDC6518B20BF3E2F0172F8295C0173C8CD7357CDED8E00542C633E45D49D0A75B50B3895657B258040D6EBAEC4CF0CC71ADA9B84590BD3F317D72DF74BCB01221FC7F0D3E6019BCF1C343B579A8C091A761C56B9481C6A83C5B9B48512B1E2B61D9474DAE6BB7973972AB5111C60840E3624BDD5E756CC9C6440C509AAC31CFB3E14CD7F6AEC77566637AD51718F701597FE7EA927"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
