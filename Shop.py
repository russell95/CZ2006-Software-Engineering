from flask import request
import pymysql

class Shop:
	#constructor
	def __init__(self, shopid, unitnum, shopname, category, mallid, mallarray):
		self.__shopid = shopid
		self.__unitnum = unitnum
		self.__shopname = shopname
		self.__category = category
		self.__mallid = mallid
		self.__mallarray = mallarray

	#get shop ID 
	def getId(self):
		return self.__shopid

	#get unit number of shop
	def getUnitNum(self):
		return self.__unitnum

	#get Shop name
	def getShopName(self):
		return self.__shopname

	#get category of shop 
	def getCategory(self):
		return self.__category

	#get mall ID 
	def getMallId(self):
		return self.__mallid

	#get array of mall information
	def getMallArray(self):
		return self.__mallarray

	#set shop ID
	def setId(self, idIn):
		self.__shopid = idIn

	#set unit number
	def setUnitNum(self, unitNumIn):
		self.__unitnum = unitNumIn;

	#set shop name
	def setShopName(self, shopnameIn):
		self.__shopname = shopnameIn

	#set shop category
	def setCategory(self, categoryIn):
		self.__category = categoryIn

	#set mall ID 
	def setMallId(self, mallId):
		self.__mallid = mallId

	#set new set if mall information
	def setMallArray(self, mallarray):
		self.__mallarray = mallarray


#Singleton for mall class, note can only be used in factory
class ShopSingleton(object):

	__shopinstance = None
	#get instance of class
	def __new__(cls, shopid, unitnum, shopname, category, mallid, mallarray):
		if cls.__shopinstance is None:
			cls.__shopinstance = Shop(shopid, unitnum, shopname, category, mallid, mallarray)
		else:
			#if there is a variable that is existing, we want to change the variables instead and return it
			cls.__shopinstance.setId(shopid)
			cls.__shopinstance.setUnitNum(unitnum)
			cls.__shopinstance.setShopName(shopname)
			cls.__shopinstance.setCategory(category)
			cls.__shopinstance.setMallId(mallid)
			cls.__shopinstance.setMallArray(mallarray)
		return cls.__shopinstance

	@classmethod
	def getInstance(cls):
		return cls.__shopinstance