from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import requests
import platform
import chromedriver_autoinstaller

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import requests
import chromedriver_autoinstaller

class GetUniWebdriver():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--headless")
        #關閉INFO:CONSOLE
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
    def darwin(self):
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        driver.implicitly_wait(5)
        return driver
    def linux(self):
        driver = webdriver.Chrome(options=self.options)
        driver.implicitly_wait(5)
        return driver
    def windows(self):
        print("下載 Chrome 自動化套件中，檔案有點大，忍耐一下。")
        chromedriver_autoinstaller.install(cwd=True)
        print("下載完成。")
        driver = webdriver.Chrome(options=self.options)
        #driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        return driver
    def others(self):
        print("Downloading Chrome Driver that Match Chrome")
        chromedriver_autoinstaller.install(cwd=True)
        print("Download OK")
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        return driver

def login(driver, url):
    driver.get(url)
    print("成功連結上 : " + driver.title)  # 印出title
    driver.set_window_size(1200, 600)


from datetime import datetime
from xlrd import xldate_as_tuple
def execl_data_to_Str(vaule):
    date = datetime(*xldate_as_tuple(vaule, 0))
    cell = date.strftime('%Y/%m/%d')
    return (cell)

def lineNotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}

    # Post 封包出去給 Line Notify
    r = requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        params=payload)
    return r.status_code


def gettext(driver, source_type, path):
    if source_type == 'id':
        gettext = driver.find_element(By.ID, path).text
    if source_type == 'xpath':
        gettext = driver.find_element(By.XPATH, path).text
    return gettext


def input(driver, source_type, path, txt):
    if source_type == 'id':
        driver.find_element(By.ID, path).send_keys(txt)
    elif source_type == 'xpath':
        driver.find_element(By.XPATH, path).send_keys(txt)


def click(driver, source_type, path):
    if source_type == 'id':
        driver.find_element(By.ID, path).click()
    elif source_type == 'xpath':
        driver.find_element(By.XPATH, path).click()
    elif source_type == 'name':
        driver.find_element(By.NAME, path).click()
    elif source_type == 'link':
        driver.find_element(By.LINK_TEXT, path).click()
    elif source_type == 'tag':
        driver.find_element(By.TAG_NAME, path).click()
    elif source_type == 'class':
        driver.find_element(By.CLASS_NAME, path).click()
    elif source_type == 'css':
        driver.find_element(By.CSS_SELECTOR, path).click()

def find_ele(driver, source_type, path):
    if source_type == 'id':
        driver.find_element(By.ID, path)
    elif source_type == 'xpath':
        driver.find_element(By.XPATH, path)
    elif source_type == 'name':
        driver.find_element(By.NAME, path)
    elif source_type == 'link':
        driver.find_element(By.LINK_TEXT, path)
    elif source_type == 'tag':
        driver.find_element(By.TAG_NAME, path)
    elif source_type == 'class':
        driver.find_element(By.CLASS_NAME, path)
    elif source_type == 'css':
        driver.find_element(By.CSS_SELECTOR, path)


def select(driver, source_type, path, txt):
    if source_type == 'id':
        Select(driver.find_element(By.ID, path)).select_by_visible_text(txt)
    elif source_type == 'xpath':
        Select(driver.find_element(By.XPATH, path)).select_by_visible_text(txt)

def action_chain_click(driver, source_type, path):
    if source_type == 'xpath':
        resp = driver.find_element(By.XPATH, path)
        ActionChains(driver).move_to_element(resp).click(resp).perform()

def flame_parent(driver):
    driver.switch_to.parent_frame()

def flame(driver, number):
    driver.switch_to.frame(number)

def windows(driver, number):
    windows = driver.window_handles
    driver.switch_to.window(windows[number])

#def sw_windows(driver, number):
#   driver.switch_to.window(windows[number])

def col_blue():return '\033[34m'
def col_green():return '\033[32m'
def col_red():return '\033[31m'
def col_yellow():return '\033[33m'
def col_yellow_down():return '\033[33m'
def col_pu():return '\033[35m'
def col_def():return '\033[0m'