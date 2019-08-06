import requests
import json
import os
import tempfile
from t_misc import *


class API(object):

	def __init__(self):
		self.token = ""
		self.username = ""
		self.chat_id = None		
		self.number_of_entries = None
		self.last_number_of_entries = None
		self.last_update_id = None	
		self.updates = None
		self.last_update = None
		#self.sp = None
		self.GetChatId()


	def ExceptionHandling(self, traceback):
		self.SendMessage("Exception found!!!\nSending report...")

		self.SendMessage(traceback)

		filename = RandomName()
		usertemp = tempfile.gettempdir()
		windowstemp = "C:\\Windows\\Temp"
		
		if os.path.exists(usertemp):
			path = (usertemp+"\\"+filename)
			file = open(path,'w')
			file.write(traceback)
			file.close()
			self.SendDocument(path)
			os.remove(path)
		elif os.path.exists(windowstemp):
			path = (windowstemp+"\\"+filename)
			file = open(path,'w')
			file.write(traceback)
			file.close()
			self.SendDocument(path)
			os.remove(path)
		else:
			self.tapi.SendMessage("Temporal directories not found!")


	def GetRequest(self, url):	
		req = requests.get(url)	
		if req.status_code == 200:
			return req
		else:
			return False


	def PostRequest(self, url, payload, headers=None, files=None):	
		req = requests.post(url, data=payload, headers=headers, files=files)
		#print("Result of POST request: %s" % req.text)		
		if req.status_code == 200:
			return req
		else:
			return False


	def GetUpdates(self): # https://core.telegram.org/bots/api#getting-updates
		url = "https://api.telegram.org/bot" + self.token + "/getUpdates"
		self.updates = self.GetRequest(url).json()


	def GetUsername(self, update):
		return update["message"]["from"]["username"]


	def GetChatId(self):
		while True:
			self.GetUpdates()
			#print("Searching chat id for username %s..." % self.username)
			for update in self.updates["result"]:
				if self.GetUsername(update) == self.username:
					self.chat_id = update["message"]["chat"]["id"]
					self.last_number_of_entries = len(self.updates["result"])
					#self.sp = self.token + ":" + self.username + ":" + str(self.chat_id)
					#print("Chat ID for username '%s' found at '%s!'" % (self.username, self.chat_id))
					return True
			time.sleep(10)


	def GetLastUpdate(self):
		self.last_update = self.updates["result"][len(self.updates["result"])-1]
		self.last_update_id = self.last_update["update_id"]


	def CleanUpdates(self):		
		#print("Cleaning updates...")
		if self.last_update_id == None:
			self.GetLastUpdate()
		url = "https://api.telegram.org/bot" + self.token + "/getUpdates?offset=" + str((int(self.last_update_id) + 1))
		result = self.GetRequest(url).json()
		if result:
			self.updates = None
			self.last_update = None
			self.last_update_id = None
			self.number_of_entries = 0
			self.last_number_of_entries = 0


	def WaitForUpdate(self, TypeOfUpdate="text"): # type = text or document
		while True:			
			time.sleep(5)
			self.GetUpdates()
			self.number_of_entries = len(self.updates["result"])
			print(self.number_of_entries)
			if self.number_of_entries > self.last_number_of_entries:
				self.last_number_of_entries = self.number_of_entries
				self.GetLastUpdate()
				if TypeOfUpdate == "text":
					if "text" in self.last_update["message"]:
						return self.last_update["message"]["text"]
					else:
						self.SendMessage("No text detected.")
				elif TypeOfUpdate == "document":
					if "document" in self.last_update["message"]:
						return self.last_update["message"]["document"]
					else:
						self.SendMessage("No document detected.")
				else:
					self.SendMessage("Type of update not supported.")
					break
			else:
				if len(self.updates["result"]) > 10:
					self.CleanUpdates()


	def SendChatAction(self, action): # https://core.telegram.org/bots/api#sendchataction
		payload = {
		  "chat_id": self.chat_id,
		  "action": action
		}

		headers = {
 		 "Content-type": "application/json; charset=utf-8"
		}

		url = "https://api.telegram.org/bot" + self.token + "/sendChatAction"

		self.PostRequest(url, json.dumps(payload), headers=headers)


	def SendMessage(self, text): # https://core.telegram.org/bots/api#sendmessage
		#print("Sending message to username '%s' with chat id '%s'..." % (self.username, self.chat_id))

		payload = {
		  "chat_id": self.chat_id,
		  "text": text
		}

		headers = {
 		 "Content-type": "application/json; charset=utf-8"
		}

		url = "https://api.telegram.org/bot" + self.token + "/sendMessage"

		self.PostRequest(url, json.dumps(payload), headers=headers)


	def SendPhoto(self, photo): # (photo = path to photo) - https://core.telegram.org/bots/api#sendphoto
		#print("Sending photo '%s' to username '%s' with chat id '%s'..." % (photo, self.username, self.chat_id))

		self.SendChatAction("upload_photo")

		payload = {
		  "chat_id": self.chat_id
		}

		files = {'photo': ("photo", open(photo, 'rb'), "multipart/form-data")}

		url = "https://api.telegram.org/bot" + self.token + "/sendPhoto"

		self.PostRequest(url, payload, files=files)


	def SendDocument(self, file): # (file = path to file) - https://core.telegram.org/bots/api#senddocument
		#print("Sending file '%s' to username '%s' with chat id '%s'..." % (file, self.username, self.chat_id))

		self.SendChatAction("upload_document")

		payload = {
		  "chat_id": self.chat_id
		}

		files = {'document': ("document", open(file, 'rb'), "multipart/form-data")}

		url = "https://api.telegram.org/bot" + self.token + "/sendDocument"

		self.PostRequest(url, payload, files=files)


	def GetFile(self, file_id): # https://core.telegram.org/bots/api#getfile

		payload = {
		  "file_id": file_id
		}

		headers = {
 		 "Content-type": "application/json; charset=utf-8"
		}

		url = "https://api.telegram.org/bot" + self.token + "/getFile"

		file_path = self.PostRequest(url, json.dumps(payload), headers=headers).json()

		return file_path["result"]["file_path"]