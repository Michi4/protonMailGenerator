from PIL import Image
import pyautogui
import time
import random
import string
import webbrowser
import ctypes
import re

CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p


def get_clip_6_digit():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value.decode("utf-8")
            kernel32.GlobalUnlock(data_locked)
            match = re.search(r'(\d{6})', value)
            return match.group(0) if match else None
    finally:
        user32.CloseClipboard()


def get_mail():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value.decode("utf-8")
            kernel32.GlobalUnlock(data_locked)
            if "@dropmail.me" in value or "@10mail.org" in value or "@emlpro.com" in value or "@emltmp.com" in value:
                match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', value)
                return match.group(0) if match else None
            return None
    finally:
        user32.CloseClipboard()


def randomize(option, length):
    characters = ''
    generated_info = ''

    if option == '-p':
        characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    elif option == '-s':
        characters = string.ascii_letters + string.digits
    elif option == '-l':
        characters = string.ascii_letters
    elif option == '-n':
        characters = string.digits
    elif option == '-m':
        characters = 'JFMASOND'

    if option == '-d':
        generated_info = str(random.randint(1, 28))
    elif option == '-y':
        generated_info = str(random.randint(1950, 2000))
    else:
        generated_info = ''.join(random.choice(characters) for _ in range(length))

    return generated_info

webbrowser.open('https://google.com')

time.sleep(5)
pyautogui.keyDown('ctrlleft')
pyautogui.keyDown('shift')
pyautogui.typewrite('p')
pyautogui.keyUp('ctrlleft')
pyautogui.keyUp('shift')
pyautogui.typewrite('https://account.proton.me/signup?plan=free\n')
time.sleep(5)

# Username
_username = randomize('-s', 5) + randomize('-s', 5) + randomize('-s', 5)
pyautogui.typewrite(_username + '\t\t')
print("Username:" + _username)

# Password
_password = randomize('-p', 16)
pyautogui.typewrite(_password + '\t' + _password + '\t')
print("Password:" + _password)

pyautogui.typewrite('\n')
time.sleep(5)
pyautogui.typewrite('\t\t\t\n')

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('t')
pyautogui.keyUp('ctrlleft')

time.sleep(10)
pyautogui.typewrite('https://dropmail.me/\n')

pyautogui.keyDown('shift')
pyautogui.keyDown('down')
pyautogui.keyUp('down')
pyautogui.keyUp('shift')
time.sleep(10)

new_mail = True
while True:
    if not new_mail:
        pyautogui.keyDown('ctrlleft')
        pyautogui.typewrite('r')
        pyautogui.keyUp('ctrlleft')
        time.sleep(5)
    pyautogui.typewrite('\t' * 28)
    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('shiftleft')
    pyautogui.keyDown('shiftright')
    pyautogui.press('down')
    pyautogui.keyUp('shiftleft')
    pyautogui.keyUp('shiftright')
    pyautogui.keyUp('ctrlleft')
    pyautogui.keyDown('ctrlleft')
    pyautogui.typewrite('c')
    pyautogui.keyUp('ctrlleft')
    new_mail = get_mail()
    if new_mail:
        print("10 min mail: " + new_mail)
        break

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(1)
# äpyautogui.typewrite(new_mail)
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('v')
pyautogui.keyUp('ctrlleft')
pyautogui.press('backspace')
pyautogui.typewrite('\n')

time.sleep(10)

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(1)

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('a')
pyautogui.keyUp('ctrlleft')
pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('c')
pyautogui.keyUp('ctrlleft')

pyautogui.keyDown('ctrlleft')
pyautogui.typewrite('\t')
pyautogui.keyUp('ctrlleft')
time.sleep(5)
pyautogui.typewrite(str(get_clip_6_digit()) + '\n')

time.sleep(5)
pyautogui.typewrite('\n')
time.sleep(5)
pyautogui.typewrite('\t\t\t\n')
time.sleep(1)
pyautogui.typewrite('\t\n')

print(_username + "@proton.me:" + _password)

logfile = open("accLog.txt", "a")
logfile.write(_username + "@proton.me:" + _password + "\n")
logfile.close()
