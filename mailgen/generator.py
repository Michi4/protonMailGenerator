import pyautogui
import time
import random
import webbrowser
import ctypes
import re

CF_TEXT = 1

SHORT_WAIT = 5
MEDIUM_WAIT = 10

USERNAME_LENGTH = 15
PASSWORD_LENGTH = 16

SKIPPED_DROPMAIL_ELEMS = 30

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p


def get_clipboard_data():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value
    finally:
        user32.CloseClipboard()


def get_clip_6digit():
    value = get_clipboard_data()
    if value is not None:
        return str(re.findall(r'(\d{6})', str(value)))
    return None


def get_mail():
    value = get_clipboard_data()
    if value is not None and any(
            suffix in str(value) for suffix in ["@dropmail.me", "@10mail.org", "@emlpro.com", "@emltmp.com"]):
        match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', str(value))
        return str(match.group(0)) if match else None
    return False


def randomize(option, length):
    """
    Options:
      -p for letters, numbers, and symbols
      -s for letters and numbers
      -l for letters only
      -n for numbers only
      -m for month selection
      -d for day selection
      -y for year selection
    """
    if length <= 0:
        raise ValueError('Length must be greater than 0')

    characters = ''

    if option == '-p':
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
    elif option == '-s':
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    elif option == '-l':
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    elif option == '-n':
        characters = '1234567890'
    elif option == '-m':
        characters = 'JFMASOND'
    elif option == '-d':
        return random.randint(1, 28)
    elif option == '-y':
        return random.randint(1950, 2000)

    return ''.join(random.choice(characters) for _ in range(length))


def get_proton_mail():
    # Open ProtonMail signup page
    webbrowser.open('https://account.proton.me/signup?plan=free\n')
    time.sleep(SHORT_WAIT)

    # Username
    username = randomize('-s', 15)
    pyautogui.typewrite(f'{username}\t\t\t')
    print(f'Username: {username}')

    # Password
    password = randomize('-p', 16)
    pyautogui.typewrite(f'{password}\t{password}')
    print(f'Password: {password}')

    # Submit the form
    pyautogui.press('enter')
    time.sleep(SHORT_WAIT)

    # Other logic

    return username, password


def get_drop_mail():
    while True:
        webbrowser.open('https://dropmail.me/\n')
        time.sleep(SHORT_WAIT)
        [pyautogui.hotkey('tab') for _ in range(SKIPPED_DROPMAIL_ELEMS)]
        pyautogui.hotkey('ctrlleft', 'c')
        new_mail = get_mail()

        if new_mail:
            return new_mail


if __name__ == '__main__':
    proton_username, proton_password = get_proton_mail()
    print(f'Proton Mail: {proton_username}@proton.me:{proton_password}')
    # Append ProtonMail credentials to the log file
    with open("accLog.txt", "w") as logfile:
        logfile.write(f'{proton_username}@proton.me:{proton_password}\n')

    drop_mail = get_drop_mail()
    print(f'Drop Mail: {drop_mail}@dropmail.me')

    # # Append DropMail credentials to the log file
    # with open("accLog.txt", "a") as logfile:
    #     logfile.write(f'{drop_mail}@dropmail.me\n')
