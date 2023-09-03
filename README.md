# Python-Keylogger.

## This is a keystroke logger made in Python. It can also send the data to a predefined email.

### Description

**Overview:**

This program captures the user's keystrokes when run and outputs them to a text file. It will specify what app/process the user was
currently using as well. For example, if the word "password" was written in mspaint, the resulting output would be "msp- password"
to the text file. After half a day, the content in the text file is erased and sent off to an email if one was defined in the code.

**Technologies:**

This program uses the pynput library for capturing keystrokes, the pywin32 and psutil libraries for obtaining process names, and various
email libraries for sending the text file to a predefined email.

**Improvements:**

This program can be built on further. It is possible to incorporate a timestamp feature so we the user's activity can be monitored more
closely. An expansion of that idea could also be to add an interface for customizing when data is sent, how data is received, and more.

### Instructions

1. To run this code, use `git clone https://github.com/J-an777/python-keylogger.git`
2. Navigate to the proper directory by doing `cd python-keylogger`
3. [Optional] From here, you can create a virtual environment in Windows if you want using 