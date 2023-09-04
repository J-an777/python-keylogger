# Python-Keylogger.

## This is a keystroke logger made in Python. It can also send the data to a predefined email.

### Description

**Overview:**

This program captures the user's keystrokes when run and outputs them to a text file. It will specify what app/process the user was
currently using as well. For example, if the word "password" was written in mspaint, the resulting output would be "msp- password"
to the text file. After half a day, the content in the text file is erased and sent off to an email if one was defined in the code.

**Technologies:**

This program uses the `pynput` library for capturing keystrokes, the `pywin32` and `psutil` libraries for obtaining process names, and various email libraries for sending the text file to a predefined email.

**Improvements:**

This program can be built on further. It is possible to incorporate a timestamp feature so we the user's activity can be monitored more
closely. An expansion of that idea could also be to add an interface for customizing when data is sent, how data is received, and more.

### Instructions

1. Make sure you are connected to the internet so that this code runs properly.

2. To run this code, use `git clone https://github.com/J-an777/python-keylogger.git`.

3. Navigate to the proper directory by doing `cd python-keylogger`.

4. ***Optional*** You can choose to go into `keylogger.py` and set up an email and [app password](https://support.google.com/mail/answer/185833?hl=en-GB#:~:text=Create%20and%20use%20app%20passwords%201%20Go%20to,is%20generated%20on%20your%20device.%208%20Select%20Done) (lines 103-105 in the code) if you want to take advantage of the email feature of this logger.

5. ***Optional*** From here, you can create a virtual environment in Windows if you want using `python -m venv env-name`.

6. ***Optional*** To activate the virtual environment in Windows, you can use `env-name\Scripts\activate`.

7. Use `pip install -r requirements.txt` to install all the dependencies.

8. You can now run the python file just as any other by using `python keylogger.py`.

9. You can terminate the script at any time by aborting: `Ctrl + C`.

### Known Issues

- There is currently no way to abort the program other than using `Ctrl + C`.
- To build this to an .exe file using PyInstaller, a 32-bit version of Python must be used due to the `pywin32` library.
- There is no default behavior for when the email or password is invalid. It will only display an error message and move on with
  clearing the file.