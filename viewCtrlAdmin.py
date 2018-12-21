from flask import Flask, render_template, request, redirect, url_for
import pymysql
import json
import mallCtrl
import shopCtrl
import parkingCtrl
import crawlCtrl
import AdminCtrl

app = Flask(__name__);

#render admin login page
@app.route('/admin')
def templateskin():
	return render_template('indexAdmin.html')

#routes login information and validates user login with database and renders redirect to the adminSelection html 
@app.route('/adminLogin',methods = ['POST'])
def adminLogin():
	if request.method == "POST":
		username = request.form['user_name']
		upassword = request.form['pass_word']
	else:
		if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
		else:
			username = AdminCtrl.checkAdminInstance().getUsername()
			upassword = AdminCtrl.checkAdminInstance().getPassword()
	retParam = AdminCtrl.checkNullUsername(username)
	retPswParam = AdminCtrl.checkNullPassword(upassword)
	if(retParam == "error"):
		return render_template('indexAdmin.html', result ="Please enter a username")
	if(retPswParam == "error"):
		return render_template('indexAdmin.html', result ="Please enter a password")
	result = AdminCtrl.chckValidAdminInDB(username)
	loginresult = AdminCtrl.checkLoginResult(result, upassword)
	if loginresult == "fail":
		return render_template('indexAdmin.html', result ="Invalid username/password")
	else:
		adminobj = AdminCtrl.createAdminObj(result)
		return render_template('adminSelectionPage.html', name=adminobj.getUsername())

#initiate web crawling and renders page with success or failure message
@app.route('/adminLogin/webscraper',methods = ['POST', 'GET'])
def webscrape():
	if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
	if request.method == "POST":
		mallname = request.form['mall']
		retParam = mallCtrl.checkNullMallName(mallname)
		if(retParam == "error"):
			return render_template('adminSelectionPage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())
		else:
			ValidResponse = crawlCtrl.checkPageResponse(mallname)
			if(ValidResponse=="error"):
				 return render_template('adminSelectionPage.html', result= "Mall Name invalid", name=AdminCtrl.checkAdminInstance().getUsername())
			else:
				mallAddr = parkingCtrl.fetchMallAddress(mallname)
				mallPostal = parkingCtrl.fetchMallPostal(mallname)
				crawlCtrl.CrawlMallFromWeb(mallname,mallAddr,mallPostal,ValidResponse)
				return render_template('adminSelectionPage.html', result= "Web Crawl Complete", name=AdminCtrl.checkAdminInstance().getUsername())
	else:
		return render_template('adminSelectionPage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())

#receive mall input from admin validates input and renders redirect to update mall page 
@app.route('/adminLogin/updateSelectionPage',methods = ['POST', 'GET'])
def updateSelectionPage():
	if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
	if request.method == "POST":
		mallname = request.form['mall']
	else:
		if(mallCtrl.checkInstance() == "empty"):
		  return render_template('home.html', result = "Session time out, please search again")
		else:
		  mallname = mallCtrl.checkInstance().getName()
	retParam = mallCtrl.checkNullMallName(mallname)
	if(retParam == "error"):
		return render_template('adminSelectionPage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())
	else:
		if(mallCtrl.checkInstance() != "empty"):
			if(mallname == mallCtrl.checkInstance().getName()):
				print("executing efficiency code")
				return render_template("adminUpdatePage.html", result=json.dumps(mallCtrl.checkInstance().getShopArray()), name=AdminCtrl.checkAdminInstance().getUsername())
		mallid = mallCtrl.retrieveMallID(mallname)
		if not mallid:
			return render_template('adminSelectionPage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())
		else:
			results = shopCtrl.retrieveAllShops(mallid)
			mallresults = mallCtrl.chckValidMallInDB(mallname)
			mallobj = mallCtrl.createMallObj(mallresults)
			validResults = shopCtrl.checkShopResults(results)
			if(validResults == "error"):
			    return render_template('adminSelectionPage.html', result ="Shop detail not available", name=AdminCtrl.checkAdminInstance().getUsername())
			else:
			    shopArray = shopCtrl.formatShopsResults(results,mallobj.getName())
			    mallobj.setShopArray(shopArray)
			    return render_template("adminUpdatePage.html", result=json.dumps(shopArray), name=AdminCtrl.checkAdminInstance().getUsername())

#route from updateQueryPage and checks for valid mall in database; returns shop info on success
@app.route('/adminLogin/updateSelectionPage/updateQueryPage',methods = ['POST', 'GET'])
def updateQueryPage():
	if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
	if request.method == "POST":
		mallname = request.form['mallquery']
	else:
		if(mallCtrl.checkInstance() == "empty"):
		  return render_template('home.html', result = "Session time out, please search again")
		else:
		  mallname = mallCtrl.checkInstance().getName()
	retParam = mallCtrl.checkNullMallName(mallname)
	if(retParam == "error"):
		return render_template('adminUpdatePage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())
	else:
		if(mallCtrl.checkInstance() != "empty"):
			if(mallname == mallCtrl.checkInstance().getName()):
				print("executing efficiency code")
				return render_template("adminUpdatePage.html", result=json.dumps(mallCtrl.checkInstance().getShopArray()), name=AdminCtrl.checkAdminInstance().getUsername())
		mallid = mallCtrl.retrieveMallID(mallname)
		if not mallid:
			return render_template('adminUpdatePage.html', result ="Mall not found", name=AdminCtrl.checkAdminInstance().getUsername())
		else:
			results = shopCtrl.retrieveAllShops(mallid)
			mallresults = mallCtrl.chckValidMallInDB(mallname)
			mallobj = mallCtrl.createMallObj(mallresults)
			validResults = shopCtrl.checkShopResults(results)
			if(validResults == "error"):
			    return render_template('adminUpdatePage.html', result ="Shop detail not available", name=AdminCtrl.checkAdminInstance().getUsername())
			else:
			    shopArray = shopCtrl.formatShopsResults(results,mallobj.getName())
			    mallobj.setShopArray(shopArray)
			    return render_template("adminUpdatePage.html", result=json.dumps(shopArray), name=AdminCtrl.checkAdminInstance().getUsername())

#route from updateQueryPage; receives shopinfo from admin; update shop and returns new shop object for display on same page
@app.route('/adminLogin/updateSelectionPage/updateShopInfo',methods = ['POST', 'GET'])
def updateShopInfo():
	if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
	if request.method == "POST":
		unitNumber = request.form['unitNum']
		oldsname = request.form['oldsname']
		shopname = request.form['sname']
		category = request.form['category']
		mallname = request.form['mname']
		
		retParam = shopCtrl.checkNullShopName(shopname)
		if(retParam=="error"):
			return render_template("adminUpdatePage.html", result="Shopname or category cannot be empty", name=AdminCtrl.checkAdminInstance().getUsername())
		else:
			mallid = mallCtrl.checkInstance().getId()
			shopid = shopCtrl.fetchShopID(unitNumber, mallid, oldsname)
			shopCtrl.updateField(shopid[0], category, shopname)
			shopArray = mallCtrl.checkInstance().getShopArray()
			for item in shopArray['values']:
				if(item['Unit'] == unitNumber and item['ShopName'] == oldsname):
					item['ShopName'] = shopname
					item['Category'] = category
					break
			mallCtrl.checkInstance().setShopArray(shopArray)
			shopArrayNew = mallCtrl.checkInstance().getShopArray()
			return render_template("adminUpdatePage.html", result=json.dumps(shopArrayNew), name=AdminCtrl.checkAdminInstance().getUsername())

#route from updateQueryPage; receives mallinfo from admin; update mall and returns new mall object for display on same page
@app.route('/adminLogin/updateSelectionPage/updateMallName',methods = ['POST', 'GET'])
def updateMallName():
	if AdminCtrl.checkAdminInstance() == "empty":
			return render_template('indexAdmin.html', result="Session timeout, please relogin")
	if request.method == "POST":
		newmallname = request.form['newmallname']
		oldmallname = request.form['oldmallname']

		retParam = mallCtrl.checkNullMallName(oldmallname)
		if(retParam=="error"):
			return render_template("adminUpdatePage.html", result="Input Field empty", name=AdminCtrl.checkAdminInstance().getUsername())
		else:
			mallid = mallCtrl.checkInstance().getId()
			mallCtrl.updateField(mallid, newmallname)
			shopArrayNew = mallCtrl.checkInstance().getShopArray()
			shopArrayNew['mname'] = newmallname
			return render_template("adminUpdatePage.html", result=json.dumps(shopArrayNew), name=AdminCtrl.checkAdminInstance().getUsername())
		



if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5001, debug=True)

