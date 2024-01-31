#! python3

import time
import random
import pyautogui
from mimesis import Generic
from mimesis.locales import Locale

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.expected_conditions import  presence_of_element_located

def sleep_random(seconds=0):
    wait = (random.randint(1 + seconds, 3 + seconds) + random.random())
    print(f'Wait: {wait}')
    time.sleep(wait)



def set_driver():
    options = Options()
    options.add_argument("-private")
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(800, 900)
    return driver


def open_dropmail(url):
    host = "droopmailme"
    while host not in ["dropmail.me",
                       "minimail.gq",
                       "yomail.info",

                       # not working
                       # "emltmp.com",
                       # "spymail.one",
                       # '10mail.tk'
                       # 'zeroe.ml'
                       ]:
        print(f"{host=}")
        driver.get(url)
        fake_email = ""
        while fake_email == "":
            fake_email = get_email()
        _, host = fake_email.split("@")

    print(f"GET {fake_email=}")
    print("First window: ", driver.title)
    sleep_random()
    return fake_email


def get_email():
    wait = WebDriverWait(driver, 50)
    try:
        wait.until(presence_of_element_located((
            By.XPATH, "/html/body/div[2]/div[3]/div/div/div/span[1]")))

        results = driver.find_elements(
            By.XPATH,
            "/html/body/div[2]/div[3]/div/div/div/span[1]")
        sleep_random()
        fake_email = results[0].text
        print(f'{fake_email=}')
        return fake_email
    except Exception as e:
        print(f"error EMAIL: {e}")
        fake_email = ""
    return fake_email


def open_proton(url):
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)
    print("Second window: ", driver.title)
    sleep_random(5)


def click_button(xpath, name=""):
    try:
        button_xpath = xpath
        button_element = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        if button_element:
            button_element.click()
            print(f"Button {name} pressed")
        else:
            print(f"Button  {name} not found")
        return button_element
    except Exception as e:
        print(f"Error button {name}: {e}")


def enter_data_signup():
    driver.find_element(By.ID, "password").send_keys(password)
    sleep_random()
    driver.find_element(By.ID, "repeat-password").send_keys(password)
    print(f'{password=}')
    sleep_random()
    driver.switch_to.frame(driver.find_element(By.CLASS_NAME, "challenge-width-increase"))
    driver.find_element(By.ID, "email").send_keys(username)
    driver.switch_to.default_content()
    print(f'{username=}')

    driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()


def enter_email(fake_email):
    sleep_random(3)
    driver.find_element(By.ID, 'label_1').click()
    sleep_random(2)
    driver.find_element(By.ID, "email").send_keys(fake_email)
    sleep_random()
    driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/main/div/div[2]/div/div[2]/button").click()
    print(f'==MY {fake_email=}')
    sleep_random(1)


def get_code_confirm():
    driver.switch_to.window(driver.window_handles[0])
    confirm_text = ""
    while confirm_text == "":
        wait = WebDriverWait(driver, 60)
        try:
            wait.until(presence_of_element_located((
                By.XPATH,
                "/html/body/div[2]/div[9]/div[2]/ul/li/div[3]/div[1]/pre")))

            results = driver.find_elements(
                By.XPATH,
                "/html/body/div[2]/div[9]/div[2]/ul/li/div[3]/div[1]/pre")
            sleep_random()
            confirm_text = results[0].text
            print(f"{confirm_text=}")

        except Exception as e:
            print(f"Error to find CODE: {e}")
            confirm_text = ""

    if len(confirm_text) > 6:
        confirm_text = confirm_text[-6:]
    return confirm_text.strip()


def enter_confirm_code(confirm):
    driver.switch_to.window(driver.window_handles[1])
    sleep_random()
    pyautogui.typewrite(confirm, interval=0.1)
    pyautogui.press('tab', presses=1)
    button_xpath = '/html/body/div[1]/div[4]/div/main/div/div[2]/button[1]'
    click_button(button_xpath, name="Enter CONFIRM")
    sleep_random()


def confirm_display_name():
    sleep_random(3)
    button_xpath = '/html/body/div[1]/div[4]/div/main/div/div[2]/form/button'
    click_button(button_xpath, name="Enter Display Name")
    sleep_random()


def confirm_recovery_email():
    sleep_random(2)
    pyautogui.press('tab', presses=2)
    pyautogui.press('enter')
    sleep_random(2)


def confirm_warning():
    sleep_random(1)
    pyautogui.press('tab', presses=1)
    pyautogui.press('enter')


def confirm_start():
    sleep_random(2)
    pyautogui.press('tab', presses=1)
    pyautogui.press('enter')


def save_user(fake_email):
    logfile = open("accLog.txt", "a")
    logfile.write(
        username + "@proton.me\t" + password + "\t" + fake_email + "\n")
    logfile.close()


if __name__ == '__main__':
    generic = Generic(locale=Locale.EN)
    username = generic.person.username() + str(random.randint(1, 100))
    password = generic.person.password(length=10)

    driver = set_driver()
    url_drop = "https://dropmail.me/en/"
    fake_email = open_dropmail(url_drop)
    url_proton = "https://account.proton.me/signup?plan=free"
    open_proton(url_proton)
    enter_data_signup()
    enter_email(fake_email)
    confirm = get_code_confirm()
    print(f"{confirm=}")
    enter_confirm_code(confirm)
    confirm_display_name()
    confirm_recovery_email()
    confirm_start()
    save_user(fake_email)