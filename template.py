import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import platform
from zipfile import ZipFile
import shutil
import undetected_chromedriver as UC
import traceback
import requests


def getLatestStableVersion():
    link = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    try:
        resp = requests.get(link, headers=headers).json()
    except:
        print("Failed to open {}".format(link))
        return None
    download_link = resp.get('channels').get(
        'Stable').get('downloads').get('chromedriver')
    if platform.system() == "Windows":
        for data in download_link:
            if data.get('platform') == 'win64':
                return data.get('url')
    if platform.system() == "Linux":
        for data in download_link:
            if data.get('platform') == 'linux64':
                return data.get('url')
    if platform.system() == "Darwin":
        for data in download_link:
            if data.get('platform') == 'mac-x64':
                return data.get('url')
    return None


def downloadLatestChromedriver():
    driver_link = getLatestStableVersion()
    if driver_link is None:
        print("Failed to get latest stable version")
        return None
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    print("Downloading latest stable version of chromedriver, please wait (also update google chrome if there is any update available) ...")
    try:
        resp = requests.get(driver_link, headers=headers).content
    except:
        print("Failed to open {}".format(driver_link))
    with open("chromedriver.zip", "wb") as f:
        f.write(resp)
    extractZip()
    os.remove("chromedriver.zip")


def extractZip():
    if not os.path.exists("chromedriver.zip"):
        return None
    with ZipFile("chromedriver.zip", 'r') as zObject:
        if platform.system() == "Windows":
            zObject.extract(
                "chromedriver-win64/chromedriver.exe", path=os.getcwd())
            if os.path.exists(os.path.join(os.getcwd(), "chromedriver.exe")):
                os.remove(os.path.join(os.getcwd(), "chromedriver.exe"))
            shutil.move(os.path.join(os.getcwd(), "chromedriver-win64/chromedriver.exe"),
                        os.path.join(os.getcwd(), "chromedriver.exe"))
            os.rmdir("chromedriver-win64")
        elif platform.system() == "Darwin":
            zObject.extract(
                "chromedriver-mac-x64/chromedriver", path=os.getcwd())
            if os.path.exists(os.path.join(os.getcwd(), "chromedriver")):
                os.remove(os.path.join(os.getcwd(), "chromedriver"))
            shutil.move(os.path.join(os.getcwd(), "chromedriver-mac-x64/chromedriver"),
                        os.path.join(os.getcwd(), "chromedriver"))
            os.rmdir("chromedriver-mac-x64")
        else:
            zObject.extract(
                "chromedriver-linux64/chromedriver", path=os.getcwd())
            if os.path.exists(os.path.join(os.getcwd(), "chromedriver")):
                os.remove(os.path.join(os.getcwd(), "chromedriver"))
            shutil.move(os.path.join(os.getcwd(), "chromedriver-linux64/chromedriver"),
                        os.path.join(os.getcwd(), "chromedriver"))
            os.rmdir("chromedriver-linux64")
        zObject.close()


def createBrowser():
    chrome_options = Options()
    # chrome_options.headless = False
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # chrome_options.add_argument("--headless=new") #uncomment to disable opening of browser window
    # chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
    # chrome_options.add_argument("--load-extension=" + os.getcwd() + "/setupvpn")
    # chrome_options.add_argument("--proxy-server=socks5://{}:{}".format(PROXY_HOST, PROXY_PORT))
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--log-level=3")
    service = Service(executable_path="chromedriver.exe")
    driver = uc.Chrome(service=service, options=chrome_options)
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    while True:
        try:
            driver = createBrowser()
            break
        except:
            traceback.print_exc()
            downloadLatestChromedriver()
            print("Download completed")
    # now use the browser variable for opening any website
    driver.get("https://google.com")
