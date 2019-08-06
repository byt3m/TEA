import random
import string
import time
import os
#from ctypes import *
#import pyAesCrypt


def FormatDate(string):
	if len(list(string)) == 1:
		string = "0" + string
		return string
	else:
		return string


def GetDate():
	date = time.localtime()
	year = str(date.tm_year)
	month = FormatDate(str(date.tm_mon))
	day = FormatDate(str(date.tm_mday))
	return (day+"/"+month+"/"+year)


def GetTime():
	date = time.localtime()
	hour = FormatDate(str(date.tm_hour))
	minute = FormatDate(str(date.tm_min))
	second = FormatDate(str(date.tm_sec))
	return (hour+":"+minute+":"+second)


def RandomName():
	return ''.join([random.choice(string.ascii_lowercase) for i in range(16)])


'''def SetWindowState(state):
	GetConsoleWindow = CDLL("Kernel32.dll").GetConsoleWindow # https://docs.microsoft.com/en-us/windows/console/getconsolewindow
	ShowWindow = CDLL("user32.dll").ShowWindow # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
	consolePtr = GetConsoleWindow()
	ShowWindow(consolePtr, state)


def Encrypt(file_path, password):
	bufferSize = 64 * 1024
	file_output = file_path + ".aes"
	pyAesCrypt.encryptFile(file_path, file_output, password, bufferSize)
	os.remove(file_path)
	return file_output


def Decrypt(file_path, password):
	bufferSize = 64 * 1024
	file_output = file_path.replace(".aes", "")
	pyAesCrypt.decryptFile(file_path, file_output, password, bufferSize)
	os.remove(file_path)
	return file_output'''