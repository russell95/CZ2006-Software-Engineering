from flask import request
import pymysql


#please do not instantiate from this Mall class directly, make use of singleton pattern and note that the singleton pattern
#can only be called in factory
class Mall(object):

	#constructor
	def __init__(self, idIn, name, address, postalcode, shoparray):
		self.__mallid = idIn
		self.__name = name
		self.__address = address
		self.__postalcode = postalcode
		self.__shoparrays = shoparray

	#get mall ID 
	def getId(self):
		return self.__mallid

	#get mall name
	def getName(self):
		return self.__name

	#get mall address
	def getAddress(self):
		return self.__address

	#get mall postal code
	def getPostalCode(self):
		return self.__postalcode

	#get array of shops in mall
	def getShopArray(self):
		return self.__shoparrays

	#set mall ID
	def setId(self, idIn):
		self.__mallid = idIn

	#set mall name 
	def setName(self, nameIn):
		self.__name = nameIn

	#set mall address
	def setAddress(self, addressIn):
		self.__address = addressIn

	#set mall postal code 
	def setPostalCode(self, postalcodeIn):
		self.__postalcode = postalcodeIn	    

	#set array of shops in mall
	def setShopArray(self, shopArray):
		self.__shoparrays = shopArray


#Singleton for mall class, note can only be used in factory
class MallSingleton(object):

	__instance = None
	#create new mall
	def __new__(cls, idIn, name, address, postalcode, shoparray):
		if cls.__instance is None:
			cls.__instance = Mall(idIn, name, address, postalcode, shoparray)
		else:
			#if there is a variable that is existing, we want to change the variables instead and return it
			cls.__instance.setId(idIn)
			cls.__instance.setName(name)
			cls.__instance.setAddress(address)
			cls.__instance.setPostalCode(postalcode)
			cls.__instance.setShopArray(shoparray)
		return cls.__instance

	@classmethod
	#get instance of class
	def getInstance(cls):
		return cls.__instance