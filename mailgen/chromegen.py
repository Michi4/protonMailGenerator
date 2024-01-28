#! python3
#Michi4
import pyautogui
import time
import random
import string
import webbrowser
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

CF_TEXT = 1

domains = [
    "dropmail.me",
    "yomail.info",
    "mailpwr.com",
]

webbrowser.open('https://google.com')
time.sleep(5)
pyautogui.keyDown('ctrlleft'); pyautogui.keyDown('shift'); pyautogui.typewrite('n'); pyautogui.keyUp('ctrlleft'); pyautogui.keyUp('shift')
pyautogui.typewrite('https://account.proton.me/signup?plan=free\n')
time.sleep(10)


def randomize(
                _option_,
                _length_
            ):

    if _length_ > 0 :

        # Options:6Ww$oRvfSVk95tyM  6Ww$oRvfSVk95tyM    
        #       -p      for letters, numbers and symbols
        #       -s      for letters and numbers
        #       -l      for letters only
        #       -n      for numbers only
        #       -m      for month selection
        #       -d      for day selection
        #       -y      for year selection

        if _option_ == '-p':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+'
        elif _option_ == '-s':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        elif _option_ == '-l':
            string._characters_='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        elif _option_ == '-n':
            string._characters_='1234567890'
        elif _option_ == '-m':
            string._characters_='JFMASOND'

        if _option_ == '-d':
            _generated_info_=random.randint(1,28)
        elif _option_ == '-y':
            _generated_info_=random.randint(1950,2000)
        else:
            _generated_info_=''
            for _ in range(0,_length_) :
                _generated_info_= _generated_info_ + random.choice(string._characters_)

        return _generated_info_

    else:
        return 'error'

# Username
_username_=randomize('-s',5)+randomize('-s',5)+randomize('-s',5)
pyautogui.typewrite(_username_ + '\t\t\t')
print("Username:" + _username_)

# Password
_password_=randomize('-p',16)
pyautogui.typewrite(_password_+'\t'+_password_+'\t')
print("Password:" + _password_)

pyautogui.typewrite('\n')
time.sleep(5)
pyautogui.typewrite('\t\t\t\n')

sessionId = None
token = _username_
isFound = False
while not isFound:
    transport = WebsocketsTransport(url="wss://dropmail.me/api/graphql/" + token + "/websocket")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql("mutation {introduceSession {id, expiresAt, addresses {address}}}")
    result = client.execute(query)
    result_mails = result['introduceSession']['addresses']
    sessionId = result['introduceSession']['id']
    newMail = result_mails[0]['address']
    print("New mail:" + newMail)
    print("Session id:" + sessionId)
    for domain in domains:
        if domain in newMail:
            print("10 min mail: " + newMail)
            isFound = True
            break

time.sleep(1)
pyautogui.typewrite(newMail)
pyautogui.typewrite('\n')

time.sleep(20)

code = ""

while len(code) == 0:
    transport = WebsocketsTransport(url="wss://dropmail.me/api/graphql/" + token + "/websocket")
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql("query ($id: ID!) {session(id:$id) { addresses {address}, mails{rawSize, fromAddr, toAddr, downloadUrl, text, headerSubject}} }")
    result = client.execute(query, variable_values={"id": f"{sessionId}"})
    print(result)
    result_mails = result['session']['mails']
    if len(result_mails) > 0:
        code = result_mails[0]['text'][-6:]
        print(f'Verification code: {code}')


pyautogui.typewrite(code + '\n')

time.sleep(5)
pyautogui.typewrite('\n')
time.sleep(5)
pyautogui.typewrite('\t\t\t\t\n')
time.sleep(1)
pyautogui.typewrite('\t\n')

print(_username_+"@proton.me:" + _password_)

logfile = open("mailgen/accLog.txt", "a")
logfile.write(_username_ + "@proton.me:" + _password_ + "\n")
logfile.close()