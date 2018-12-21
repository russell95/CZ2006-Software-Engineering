import pymysql
import json
import AdminFactory
import Admin

#check if admin instance exist
def checkAdminInstance():
	if Admin.AdminSingleton.getAdminInstance() is None:
		return 'empty'
	else:
		return Admin.AdminSingleton.getAdminInstance()

#check if admin username is null
def checkNullUsername(username):
	if not username:
		return "error"
	else:
		return "pass"

#check if admin password is null
def checkNullPassword(password):
	if not password:
		return "error"
	else:
		return "pass"

#check if admin username is valid
def chckValidAdminInDB(username):
	conn = pymysql.connect(host='localhost', 		#Connect to database
						  database='navimalldb',
						  user='admin',
						  password='adminAccept')
	cur = conn.cursor()
	cur.execute("SELECT * FROM admin WHERE Username = %s", username)
	result = cur.fetchone()
	cur.close()
	conn.close()
	return result

#check if admin password matches with the respective password in database
def checkLoginResult(result, password):
	if not result:
		return "fail"
	elif str(result[1]) == password:
		return "success"
	else:
		return "fail"

#create admin object
def createAdminObj(result):
	__adminsingletonobj = AdminFactory.AdminFactory.makeAdminObj(result[0], result[1])
	return __adminsingletonobj

#check if admin instance exist
def checkInstance():
	if Admin.AdminSingleton.getAdminInstance() is None:
		return 'empty'
	else:
		return Admin.AdminSingleton.getAdminInstance()
