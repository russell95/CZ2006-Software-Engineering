from flask import request
import pymysql

#Admin class containing username and password and their respective getter and setters
class Admin:
	#constructor 
	def __init__(self, username, password):
		self.__username = username
		self.__password = password

	#get admin user name
	def getUsername(self):
		return self.__username

	#get admin password
	def getPassword(self):
		return self.__password

	#set admin user name 
	def setUsername(self, usernameIn):
		self.__username = usernameIn

	#set admin password
	def setPassword(self, passwordIn):
		self.__password = passwordIn

#Construction of Admin Object
class AdminSingleton(object):

	__admininstance = None
	#create new admin instance
	def __new__(cls, username, password):
		if cls.__admininstance is None:
			cls.__admininstance = Admin(username, password)
		else:
			cls.__admininstance.setUsername(username)
			cls.__admininstance.setPassword(password)
		return cls.__admininstance

	@classmethod
	#get admin instance
	def getAdminInstance(cls):
		return cls.__admininstance