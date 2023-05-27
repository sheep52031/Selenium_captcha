import os
import time
import random

import requests
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from vision import recognize_captcha

# GCP Vision API key
api_key = os.environ.get('API_KEY', '')


company_code = input(str("請輸入統編號碼:"))

# Get Driver
service = Service("./chromedriver_mac_arm64/chromedriver.exe")
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = Chrome(service=service,options = chrome_options)


#  Navigate to the website using Selenium
url = "https://www.etax.nat.gov.tw/etwmain/etw113w1/ban/query"
driver.get(url)
driver.maximize_window()
time.sleep(3)


# Set a maximum number of attempts to solve the captcha
max_attempts = 5
attempts = 0


# Define a function to check if the error modal is visible
def error_modal_visible(driver):
    try:
        modal_body = driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/jhi-dialog/div/div[2]")
        if "驗證碼錯誤" in modal_body.text:
            return True
        else:
            return False
    except NoSuchElementException:
        return False


def extract_data(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")

    data_labels = {
        "營業人統一編號": "",
        "營業狀況": "",
        "負責人姓名": "",
        "營業人名稱": "",
        "營業（稅籍）登記地址": "",
        "資本額(元)": "",
        "組織種類": "",
        "設立日期": "",
        "登記營業項目": "",
    }

    for li in soup.select("ul.etw-list-data li"):
        label = li.find("div", class_="col-6 col-md-3")
        value = li.find("div", class_="col-6 text-right text-md-left")

        if label and value:
            label_text = label.get_text(strip=True)
            value_text = value.get_text(strip=True).replace('\n', ', ')

            if label_text in data_labels:
                data_labels[label_text] = value_text

    return data_labels


def element_exists(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except NoSuchElementException:
        return False


while attempts < max_attempts:

    # Locate the input field using Selenium's find_element_by_id() method
    # Type the company_code one character at a time with a random delay between each character
    input_field = driver.find_element(By.ID,"ban")
    input_field.clear()
    for char in company_code:
        input_field.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))  # Adjust the range of delay as needed


    # Extract the image source using BeautifulSoup

    soup = BeautifulSoup(driver.page_source, "html.parser")
    img = soup.find("img", {"alt": "圖形驗證碼"})
    img_src = img["src"]
    print(img_src)
    url = "https://www.etax.nat.gov.tw"

    # Ensure the image source is a complete URL
    if not img_src.startswith("http"):
        img_src = url+img_src

    # Step 6: Download the image and save it to the desired folder
    try:
        jpg = requests.get(img_src)
        print(type(jpg))
    except:
        print("----------error-------------")


    # Make sure the 'static' folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    # Save the image to the 'static' folder
    image_path = f"static/{company_code}.jpg"

    # Save the image to the 'static' folder
    with open(image_path, "wb") as f:
        f.write(jpg.content)
        print("Image downloaded and saved to the 'static' folder.")

    # Replace with the path to your captcha image
    captcha_text = recognize_captcha(api_key, image_path)
    captcha_text = captcha_text.replace(" ", "")


    # Locate the captcha input field by its ID or any other suitable attribute
    captcha_input = driver.find_element(By.ID, "captchaText")

    # Fill in the recognized captcha value
    for char in captcha_text:
        captcha_input.send_keys(char)
        time.sleep(random.uniform(0.1, 0.5))

    time.sleep(5)

    # Locate the "Submit" button by its text, ID, or any other suitable attribute
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), '確認送出')]")


    # Click the "Submit" button
    submit_button.click()

    time.sleep(5)

    # Check if the specified XPath element is present on the page
    xpath_to_check = '//*[@id="etwMainContent"]/div[2]/div/div[2]/jhi-main/etw113w1-ban-query-result/div[1]/div[1]/h3'
    if element_exists(driver, xpath_to_check):
        break

    else:
        try:
            # Check if the error modal is visible
            if error_modal_visible(driver):
                driver.find_element(By.XPATH, "/html/body/ngb-modal-window/div/div/jhi-dialog/div/div[3]/div/button").click()

            # Clear the captcha input field
            captcha_input.clear()

            # Increment the attempts counter
            attempts += 1
        except:
            break

if attempts == max_attempts:
    print("Failed to solve the captcha after", max_attempts, "attempts.")
else:
    print("Captcha solved!")

data = extract_data(driver)
print(data)


time.sleep(30)

# Close the web driver
driver.quit()



