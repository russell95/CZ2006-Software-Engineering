import pymysql
import json
import Shop
import csv
import datetime
import requests 
import math

#onemap API to convert SVY21 based X and Y coordinates to Latitude and Longtitude 
def fetchLongLat(x,y):
    url = 'https://developers.onemap.sg/commonapi/convert/3414to4326?X='+ str(x) +'&Y='+str(y)
    jsonResult = requests.get(url).json()
    longitude = jsonResult['longitude']
    latitude = jsonResult['latitude']
    return longitude,latitude

#finds nearby HDB parking within 800 metres; return boolean value
def match(x2,y2, mallCoordinates):	
	x1 = mallCoordinates['X']
	y1 = mallCoordinates['Y']

	distance = math.sqrt( ((float(x1)-float(x2))**2) + ((float(y1)-float(y2))**2) )
	if(distance < 800):
		return True 

	return False
    
#formats nearby HDB parking results based on matched nearby mall referenced by array[index]; return json of nearby parking detail
def format(index, array):
    info = ""
    with open('hdb-carpark-information.csv', encoding = 'ISO-8859-1') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if(row['address']==array[index]):
                carparkNum = row['car_park_no']
                Long,lat = fetchLongLat(row['x_coord'],row['y_coord'])
                info = {'carpark': row['address'], 'types': row['type_of_parking_system'],
                        'short_term': row['short_term_parking'], 'free': row['free_parking'],
                        'night': row['night_parking'],'carparkNum': row['car_park_no'],'lat':lat,'long':Long} 

                break
    return info


#make data-gov API call to format; return json result of mall parking information
def formatMallParkingResults(ret_data):
    url = 'https://data.gov.sg/api/action/datastore_search?resource_id=e2468b11-6cac-42e4-8891-145c4fc1cba2&limit=1&q="'+ret_data+'"'
    jsonResult = requests.get(url).json()
    
    for item in jsonResult['result']['records']:
        carpark = item['carpark']
        rate1 = item['weekdays_rate1']
        rate2 = item['weekdays_rate2']
        sat_rate = item['saturday_rate']
        sun_hol = item['sunday_public_holiday_rate']

        rates = {'carpark': carpark, 'rate1': rate1,
                        'rate2': rate2, 'sat_rate': sat_rate, 
                                'sun_hol': sun_hol}
                    
        jsonRates = json.dumps(rates)

        return jsonRates

#make onemap API call to obtain address of mall; return Address
def fetchMallAddress(mallname):

	url ='https://developers.onemap.sg/commonapi/search?searchVal='+mallname+'&returnGeom=Y&getAddrDetails=Y&pageNum=1'
	jsonResult = requests.get(url).json()
	for item in jsonResult['results']:
		mallAddr = (item['ROAD_NAME'])
		break

	return mallAddr

#make onemap API call to obtain postal code of mall; return Postal code
def fetchMallPostal(mallname):

    url ='https://developers.onemap.sg/commonapi/search?searchVal='+mallname+'&returnGeom=Y&getAddrDetails=Y&pageNum=1'
    jsonResult = requests.get(url).json()
    for item in jsonResult['results']:
        mallPostal = (item['POSTAL'])
        break

    return mallPostal

#make onemap API call to obtain X and Y coordinates of mall; return XY coordinates 
def fetchMallCoordinates(mallname):

	url ='https://developers.onemap.sg/commonapi/search?searchVal='+mallname+'&returnGeom=Y&getAddrDetails=Y&pageNum=1'
	jsonResult = requests.get(url).json()
	for item in jsonResult['results']:
		X = (item['X'])
		Y = (item['Y'])
		break

	jsonCoordinates = {'X':X, 'Y':Y}

	return jsonCoordinates

#format and return json object of NearbyparkingResults
def formatNearbyparkingResults(mallCoordinates):

	array = []
	count = 0
	with open('hdb-carpark-information.csv', encoding= 'ISO-8859-1') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			value = match(row['x_coord'],row['y_coord'], mallCoordinates)
			if(value==True and (count < 5) ):
				array.append(row['address'])
				count = count + 1

	i =0
	size = len(array)
	nearbyInfo = []
	while i<size :
		nearbyInfo.append(format(i,array))
		i = i+1

	array.clear()
	jsonNearbyRates = json.dumps(nearbyInfo)
	return jsonNearbyRates



