from flask import Flask
import pymysql
import json
import Shop
import ShopFactory

#retrieve all shop details
def retrieveAllShops(mallID):
	results  = retrieveAllShopsDB(mallID)
	return results;

#check if shop result is empty
def checkShopResults(results):
	if not results:
		return "error"
	else:
		return "pass"

#format shop information into json object
def formatShopsResults(results, mallname):
	if not results:
		return "error"
	else:
	    shopArray = {'mname':mallname, 'values':[]}
	    for row in results:
	    	shopContent = {'ShopName': row[2], 'Unit': row[1], 'Category': row[3]}
	    	shopArray['values'].append(shopContent)
	    	shopContent = {}
	    return shopArray

#check if entered shopname is empty
def checkNullShopName(shopname):
	if not shopname:
		return "error"
	else:
		return "pass"

#retrieve all shops that matches specified mall ID
def retrieveAllShopsDB(mallID):
	conn =pymysql.connect(host='localhost',  		
                          database='navimalldb',
                          user='user',
                          password='userAccept')
	cur = conn.cursor()
	cur.execute("SELECT * FROM shop WHERE MallID=%s ORDER BY UnitNum", mallID)
	results = cur.fetchall()
	cur.close()
	conn.close
	return results

#return shop details that matches specifed shopname input
def chckValidShopInDB(shopname):
	conn = pymysql.connect(host='localhost', 		
						   database='navimalldb',
						   user='user',
						   password='userAccept')
	cur = conn.cursor()
	cur.execute("SELECT * FROM shop WHERE ShopName LIKE %s", (shopname+"%"))
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

#calls Factory to create a Shop singleton
def createShopObj(results):
	__shopSingletonObj = ShopFactory.ShopFactory.makeShopObj(results[0], results[1], results[2], results[3], results[4], [])
	return __shopSingletonObj

#send shopid, category and shopname into update function to udpate
def updateField(shopid, category, shopname):
  	update(shopid, category, shopname)

#connects to database to update specified parameters
def update(shopid, category, shopname):
	conn =pymysql.connect(host='localhost',
							database='navimalldb',
							user='admin',
							password='adminAccept')
	cur = conn.cursor()
	cur.execute("UPDATE shop SET ShopName = '{}',Category = '{}' WHERE ShopID = {}".format(shopname,category,shopid))
	conn.commit()
	cur.close()
	conn.close

#retrieve unique shop ID based on the MallID, UnitName and ShopName referenced
def retrieveShopID(unitNum, mallid, shopname):


    conn =pymysql.connect(host='localhost',      
                          database='navimalldb',
                          user='user',
                          password='userAccept')
    cur = conn.cursor()
    cur.execute("SELECT ShopID FROM shop WHERE MallID={} AND UnitNum='{}' AND ShopName='{}'".format(mallid,unitNum,shopname))
    results = cur.fetchone()
    cur.close()
    conn.close
    return results

#fetch shop ID of old shopname
def fetchShopID(unitNum, mallid, oldsname):
  results = retrieveShopID(unitNum, mallid, oldsname)
  return results;

