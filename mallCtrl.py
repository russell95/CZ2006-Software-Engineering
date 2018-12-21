import pymysql
import json
import MallFactory
import Mall

#check if mall name is null
def checkNullMallName(mallname):
	if not mallname:
	    return "error"
	else:
	    return "pass"

#retrieve mall ID 
def retrieveMallID(mallname):
	mallid = retrieveMallIdDB(mallname)
	return mallid

#format mall results in json format
def formatMallResults(results,shopname):
	mallArray = {'sname':shopname, 'values':[]}
	for row in results:
		mallContent = {'MallName': row[0]}
		mallArray['values'].append(mallContent)
		mallContent = {}
	return mallArray

#retrieve malls given the shop name
def retrieveAllMalls(shopname):
	results = retrieveAllMallsDB(shopname)
	return results

#check if the result consisting of mall is null
def checkMallResults(result):
	if not result:
		return "error"
	else:
		return "pass"

#retrieve mall ID from database given the mall name and return the result
def retrieveMallIdDB(mallname):
	conn = pymysql.connect(host='localhost',  		
                          database='navimalldb',
                          user='user',
                          password='userAccept')
	cur = conn.cursor()
	cur.execute("SELECT MallID FROM mall WHERE MallName= %s", mallname)
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

#retrieve malls that contains the specified shop
def retrieveAllMallsDB(shopname):
	conn = pymysql.connect(host='localhost', 		
						  database='navimalldb',
						  user='user',
						  password='userAccept')
	cur = conn.cursor()
	cur.execute("SELECT MallName FROM shop,mall WHERE shop.ShopName LIKE %s AND shop.MallID = mall.MallID GROUP BY MallName", (shopname + "%"))
	result = cur.fetchall()
	cur.close()
	conn.close()
	return result

#check if the mall is valid in database as well as retrieving all mall details
def chckValidMallInDB(mallname):
	conn = pymysql.connect(host='localhost', 		
						  database='navimalldb',
						  user='user',
						  password='userAccept')
	cur = conn.cursor()
	cur.execute("SELECT * FROM mall WHERE MallName = %s", mallname)
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

#calls Mall Factory to create a mall singleton 
def createMallObj(results):
	__mallSingletonObj = MallFactory.MallFactory.makeMallObj(results[0], results[1], results[2], results[3], [])
	return __mallSingletonObj

#checks if the instance of mall singleton is empty
def checkInstance():
	if Mall.MallSingleton.getInstance() is None:
		return 'empty'
	else:
		return Mall.MallSingleton.getInstance()

#sends value of mall ID and mallname to update function
def updateField(mallid, Newmallname):
  	update(mallid, Newmallname)

#connects to database and updates values based on specified parameter
def update(mallid, Newmallname):
    conn =pymysql.connect(host='localhost',      
                          database='navimalldb',
                          user='admin',
                          password='adminAccept')

    cur = conn.cursor()
    cur.execute("UPDATE mall SET MallName = '{}' WHERE MallID = {}".format(Newmallname,mallid))  
    conn.commit()
    cur.close()
    conn.close
