from datetime import *
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Chrome option controlled by software
def chrome_options():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument("--disable-extensions")
    prefs = {"profile.default_content_setting_values.notifications": 1}
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options


pw_us_path = 'pw.txt'


def pw_encription():
    pw = "<PWHERE>"
    return pw


def user_encription():
    user = "<EMAILHERE>"
    return user


def sign_in_google(EMAIL, PW):

    driver.get(url_google)

    # Email sign in
    username_inpt = driver.find_element_by_id("identifierId")
    username_inpt.send_keys(EMAIL)

    time.sleep(0.5)
    next_button = driver.find_element_by_id("identifierNext")
    next_button.click()
    # Password sign in, check if site is loaded
    password_inpt = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_inpt.send_keys(PW)

    time.sleep(0.5)
    next_button = driver.find_element_by_id("passwordNext")
    next_button.click()


def click_music_video():
    music_video = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "video-title"))
    )
    music_video.click()
    yt_dark_theme()


def select_480_quality():
    div_list = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    time.sleep(2)
    try:
        for div in div_list:
            try:
                settings_button = driver.find_element_by_xpath(
                    f'//*[@id="movie_player"]/div[{div}]/div[2]/div[2]/button[3]')
                settings_button.click()
            except:
                continue

        time.sleep(2)
        quality_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="ytp-id-18"]/div/div/div[4]/div[1]'))
        )
        quality_button.click()

        time.sleep(0.5)
        quality_480 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ytp-id-18"]'))
        )
        quality_480.click()
    except:
        pass


def yt_dark_theme():
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'img'))
    )
    account_button.click()

    dark_theme_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/ytd-app/ytd-popup-container/iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[2]/div[2]/ytd-toggle-theme-compact-link-renderer/div[2]'))
    )
    dark_theme_button.click()

    dark_theme_toggle = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'toggleButton'))
    )
    dark_theme_toggle.click()
    account_button.click()


def yt_white_theme():
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'img'))
    )
    account_button.click()

    dark_theme_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/ytd-app/ytd-popup-container/iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[2]/div[2]/ytd-toggle-theme-compact-link-renderer/div[2]'))
    )
    dark_theme_button.click()

    while True:
        try:
            dark_theme_toggle = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'toggleButton'))
            )
            dark_theme_toggle.click()
            break
        except:
            continue


def ad_skip():
    l_of_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for letter in l_of_letters:
        try:
            driver.find_element_by_xpath(
                f'//*[@id="skip-button:{letter}"]/span')
            time.sleep(5)
            skipper = driver.find_element_by_xpath(
                f'//*[@id="skip-button:{letter}"]/span/button')
            skipper.click()
            break
        except:
            continue


# Site options
def reload_site():
    driver.refresh()
    ad_skip()


def mute_video():
    mute_button = driver.find_element_by_css_selector(
        '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > span > button')
    mute_button.click()


def next_music_video():
    try:
        next_music_button = driver.find_element_by_css_selector(
            '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-next-button.ytp-button')
        next_music_button.click()
        ad_skip()
    except:
        print('Already on the last video')


def previous_music_video():
    try:
        prev_music_video = driver.find_element_by_css_selector(
            '#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > a.ytp-prev-button.ytp-button')
        prev_music_video.click()
        time.sleep(0.2)
        prev_music_video.click()
        ad_skip()
    except:
        print('Already on the first video')


def web():

    sign_in_google(user_encription(), pw_encription())
    click_music_video()
    select_480_quality()


urlYT = 'http:www.youtube.com'
url_google = "https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3D%252Fplaylist%253Flist%253DPLidVMna4T1JJ51OvohcYYwbEKoZtzBxUK&hl=en&ec=65620"

chrome_driver_path = 'chromedriver.exe'


driver = webdriver.Chrome(
    executable_path=chrome_driver_path, options=chrome_options())
# driver.set_window_position(-10000, 0)
driver.maximize_window()
driver.get(url_google)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, 'html.parser')

web()
theme = 'dark'

while True:
    inpt = input(
        '"exit", "win", "next", "prev", "mute", "rel", "min", "white", "dark": ')

    if inpt == 'exit':
        driver.quit()
        exit()
    elif inpt == 'win':
        driver.set_window_position(400, 225)
        driver.maximize_window()
    if inpt == 'next':
        next_music_video()
    elif inpt == 'prev':
        previous_music_video()
    elif inpt == 'mute':
        mute_video()
    elif inpt == 'rel':
        reload_site()
    elif inpt == 'min':
        driver.set_window_position(-10000, 0)
    elif inpt == 'dark':
        if theme == 'white':
            yt_dark_theme()
            theme = 'dark'
        else:
            print('Already in dark theme')
    elif inpt == 'white':
        if theme == 'dark':
            yt_white_theme()
            theme = 'white'
        else:
            print('Already on white theme')
    else:
        print('Invalid Input')
