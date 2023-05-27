
# Overview
This repository contains Python code that automates form submission to the Taiwan Electronic Tax Filing System (etax.nat.gov.tw). It uses Selenium for web scraping and the Google Cloud Vision API for captcha solving.

可自動向台灣電子報稅系統 (etax.nat.gov.tw) 提交表單。它使用 Selenium 進行網頁抓取，使用 Google Cloud Vision API 進行驗證碼解析。

## Prerequisites
* Python 3
* Selenium WebDriver
* BeautifulSoup4
* Google Cloud Vision API
* python-dotenv
* requests

## Installation
1. Install the required Python packages.
```bash
pip install -r requirements.txt
```
2. Download the appropriate **WebDriver** for your version of Chrome and move it to the project directory.
`https://chromedriver.chromium.org/downloads`
下載適用於您的 Chrome 版本的 WebDriver 並將其移動到專案資料夾中

3. Set up your environment variables in a `.env` file.

```.env
YOUR_SERVICE=your-google-cloud-credentials.json
API_KEY=your-google-cloud-vision-api-key
```

Replace `your-google-cloud-credentials.json` with the path to your Google Cloud credentials JSON file and `your-google-cloud-vision-api-key` with your actual API key.

## Usage
```bash
python main.py
```

You will be prompted to enter a company code (統一編號). The script will automatically fill the form, solve the captcha, and submit the form. If successful, it will print the business information associated with the entered company code.
系統會提示您輸入公司代碼（統一編號）。該腳本將導航到網站、填寫表格、解決驗證碼並提交表格。如果成功，它將打印與輸入的公司代碼關聯的業務信息。

* Entering the company code into the form one character at a time with a random delay between each character
將公司代碼一次輸入一個字符，每個字符之間有隨機延遲

* Extracting the captcha image and saving it to the local filesystem
提取驗證碼圖像並將其保存到本地文件系統

* Recognizing the captcha text with the Google Cloud Vision API
使用 Google Cloud Vision API 識別驗證碼文本

* Filling in the captcha text and submitting the form
填寫驗證碼文本並提交表單

* If the captcha is solved successfully, the business information is printed. Otherwise, the process is attempted again for a maximum of five attempts.
如果驗證成功，則打印業務信息。否則，將再次嘗試該過程，最多嘗試五次