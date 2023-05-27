
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
# GCP VISION API Service Account credentials
YOUR_SERVICE=your-google-cloud-credentials.json
API_KEY=your-google-cloud-vision-api-key
```

Replace `your-google-cloud-credentials.json` with the path to your Google Cloud credentials JSON file and `your-google-cloud-vision-api-key` with your actual API key.


## Setting up GCP Service Account and downloading the credentials JSON

1. Create a Google Cloud Project
* Head to the Google Cloud Console (console.cloud.google.com).
* If you haven't already created a project, click on the project drop-down and select 'New Project', and then set the project name and location.

1. Enable Google Vision API
* Navigate to the "Library" section in the left-hand side menu.
* Search for "Vision API" and select it from the results.
On the API page, click "Enable".

1.  Create a Service Account
* Go to the "IAM & Admin" -> "Service accounts" section in the left-hand side menu.
* Click "Create Service Account" at the top.
* Enter a name for the service account and add a description.
* Click "Create".

1. Grant permissions to the Service Account
* On the "Service account permissions" page, select the "Role" as 'Project' -> 'Owner'.
* Click "Continue".

1. Generate a JSON Key for the Service Account

* On the "Grant users access to this service account" page, click on the "Create Key" button.
* In the dialog box that appears, select "JSON" as the Key type.
* Click "Create".

6. Download the JSON Key
* Your browser will automatically download a JSON file containing the credentials for your new service account. Save this file to a secure location. You will use this file to authenticate your application with the Google Vision API.

7. Update your script
* Replace 'YOUR_SERVICE' in your script with the path to your downloaded JSON file. For example, if your JSON file is called 'linux-00-78670b5fdf42.json' and is in the same directory as your script, you would do the following:

This will set up the environment variable 'GOOGLE_APPLICATION_CREDENTIALS' with the path to your credentials file. This is how the Google Vision API knows how to authenticate your requests.

Remember not to expose your JSON credentials file publicly, as it contains sensitive information that could be used to access and control your Google Cloud resources.


## Usage run the script
```bash
python main.py
```

After you've finished setting up your environment and installing the necessary dependencies, you can run the script. You'll need to enter the Unified Business Number (UBN) of the company you're interested in when prompted. The script will then try to bypass the captcha and retrieve information about the company.
完成環境設置並安裝必要的依賴項後，您可以運行腳本。出現提示時，您需要輸入您感興趣的公司的統一業務編號 (UBN)。然後該腳本將嘗試繞過驗證碼並檢索有關公司的信息。

The script starts by asking for the UBN:
```python 
company_code = input(str("Please enter the Unified Business Number:"))
```
It then initializes a web driver and navigates to the desired URL. You'll need the appropriate chromedriver executable for this to work. The script uses the 'eager' page load strategy, meaning it will start interacting with the page as soon as the DOM is interactive.
然後它會初始化 Web 驅動程序並導航到所需的 URL。您需要適當的 chromedriver 可執行文件才能工作。該腳本使用“eager”頁面加載策略，這意味著它會在 DOM 交互時立即開始與頁面交互。

```python 
service = Service("./chromedriver_mac_arm64/chromedriver.exe")
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = Chrome(service=service,options = chrome_options)
```

After that, the script enters a loop where it tries to bypass the captcha. It does this by downloading the captcha image, using the Vision API to recognize the text in the image, and then entering that text into the captcha input field. If it fails, it will try again until it reaches the maximum number of attempts.
腳本進入一個循環，試圖繞過驗證碼。它通過下載驗證碼圖像，使用 Vision API 識別圖像中的文本，然後將該文本輸入驗證碼輸入字段來實現這一點。如果失敗，它將重試，直到達到最大嘗試次數。

If the script successfully bypasses the captcha and retrieves the information, it will print out the company data in the terminal:
如果腳本成功繞過驗證碼並檢索到訊息，它將在終端中打印出公司數據：

```python
data = extract_data(driver)
print(data)
```

Finally, the script waits for 30 seconds before closing the web driver. This gives you some time to see the results before the browser window closes:
最後，腳本在關閉 Web 驅動程序之前等待 30 秒。這使您有時間在瀏覽器窗口關閉之前查看結果：

```python 
time.sleep(30)
driver.quit()
```