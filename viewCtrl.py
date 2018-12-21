from flask import Flask, render_template, request, redirect, url_for
import pymysql
import json
import mallCtrl
import shopCtrl
import parkingCtrl

#initializes a Flask application 
#Each route defines an entry point for a redirection in the HTML page
app = Flask(__name__)

#Renders on run of view controller to render start of client page
@app.route('/')
def templateskin():
	return render_template('home.html')

#Routes from home.html to validate specified mallname and renders a redirection to mallResult Page 
@app.route('/mallResults',methods = ['POST', 'GET'])
def mallResults():
	if request.method == "POST":
		mallname = request.form['mall']
	else:
		if(mallCtrl.checkInstance() == "empty"):
		  return render_template('home.html', result = "Session time out, please search again")
		else:
		  mallname = mallCtrl.checkInstance().getName()

	retParam = mallCtrl.checkNullMallName(mallname)
	if(retParam == "error"):
		return render_template('home.html', result ="Mall not found")
	else:
		result = mallCtrl.chckValidMallInDB(mallname)
		if result:
			mallobj = mallCtrl.createMallObj(result)
		else:
			return render_template('home.html', result ="Mall not found") 
		mallid = mallCtrl.retrieveMallID(mallobj.getName())
		results = shopCtrl.retrieveAllShops(mallid)
		validResults = shopCtrl.checkShopResults(results)
		if(validResults == "error"):
			return render_template('home.html', result ="Shop detail not available")
		else:
			shopArray = shopCtrl.formatShopsResults(results,mallobj.getName())
			mallobj.setShopArray(shopArray)
			return render_template("mallResults.html", result=json.dumps(shopArray))

#Routes from home.html to validate specified shopname and renders a redirection to shopResult Page 
@app.route('/shopResults',methods = ['POST', 'GET'])
def shopResults():
	if request.method == "POST":
		shopname = request.form['shop_enter']
		retParam = shopCtrl.checkNullShopName(shopname)
		if(retParam == "error"):
			return render_template('home.html', result="Invalid shop")
		else:
			result = shopCtrl.chckValidShopInDB(shopname)
			if result:
				shopobj = shopCtrl.createShopObj(result)
			else:
				return render_template('home.html', result ="Shop not found")
			results = mallCtrl.retrieveAllMalls(shopobj.getShopName())
			validResults = mallCtrl.checkMallResults(results)
			if(validResults == "error"):
				return render_template('home.html', result="Invalid shop name")
			else:
				mallArray = mallCtrl.formatMallResults(results,shopobj.getShopName())
				shopobj.setMallArray(mallArray)
				return render_template("shopResults.html", result=json.dumps(mallArray))

#Routes from mallResults.html to send mall parkign information to parkingResult html
@app.route('/parkingResults',methods = ['POST', 'GET'])
def parkingResults():
	    if(mallCtrl.checkInstance() == "empty"):
	    	return render_template("home.html", result="Session time out, please search again")
	    else:
	    	mallCoordinates = parkingCtrl.fetchMallCoordinates(mallCtrl.checkInstance().getName())
	    	malladdress = parkingCtrl.fetchMallAddress(mallCtrl.checkInstance().getName())
	    	mallParkingInfo = parkingCtrl.formatMallParkingResults(mallCtrl.checkInstance().getName())
	    	nearbyParkingInfo = parkingCtrl.formatNearbyparkingResults(mallCoordinates)
	    	return render_template("parkingResults.html", result=mallParkingInfo, result2= nearbyParkingInfo)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
