from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
import re
import json
import mechanicalsoup
import re
import pymysql


firstnum = 1
lastnum = 9
arrayShopName = []
arrayUnitNum = []
arrayCategory = []

#retrieve categories of shops from web crawling and match them to the predefined categories displayed in the website
def recategorize():

        conn =pymysql.connect(host='localhost',
                                       database='navimalldb',
                                       user='admin',
                                       password='adminAccept')
        c = conn.cursor()
        c.execute("""UPDATE shop 
                    SET Category = 'Beauty' 
                    WHERE ShopID IN (SELECT * FROM (SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Beauty%' OR Category LIKE '%Hair%')temp) """)
        c.execute("""UPDATE shop SET Category = 'Halal F&B' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Halal F&B%')temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Beauty' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Fashion%' OR Category LIKE '%Apparel%' OR Category LIKE '%Clothing%')temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Electronics' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Electronics%' OR Category LIKE '%Telecommunication%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Food & Beverages' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Food%' OR Category LIKE '%Restaurant%' OR Category LIKE '%Bakery%')temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Sports' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Sports%')temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Education' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Education%')temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Supermarket' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Supermarket%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Pet Shop' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Pet Shop%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Entertainment' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Entertainment%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Jewellery' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Jewellery%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Bank' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category LIKE '%Bank%' )temp) """)
        c.execute("""UPDATE shop 
                    SET Category = 'Others' 
                    WHERE ShopID IN (SELECT * FROM(SELECT ShopID 
                                    FROM shop 
                                    WHERE Category NOT LIKE '%Beauty%' AND Category NOT LIKE '%Hair%' 
                                                    AND Category NOT LIKE '%Halal F&B%' 
                                                    AND Category NOT LIKE '%Fashion%' 
                                                    AND Category NOT LIKE '%Apparel%'  AND Category NOT LIKE '%Clothing%'
                                                    AND Category NOT LIKE '%Electronics%' AND Category NOT LIKE '%Telecommunication%' 
                                                    AND Category NOT LIKE '%Food%' AND Category NOT LIKE '%Restaurant%' 
                                                    AND Category NOT LIKE '%Bakery%' AND Category NOT LIKE '%Sports%'
                                                    AND Category NOT LIKE '%Education%' AND Category NOT LIKE '%Supermarket%'
                                                    AND Category NOT LIKE '%Pet Shop%' AND Category NOT LIKE '%Entertainment%'
                                                    AND Category NOT LIKE '%Jewellery%' AND Category NOT LIKE '%Bank%')temp) """)
        conn.commit()

        c.close()
        conn.close()


#checks if there is more than 8 pages in the results from the web crawling
def checkpage(url, lastnum, id1, id2): 

        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(),"html.parser")
        mall = soup.findAll("a", {"title": "Show Next 8 Page(s)"})

        if mall:
                crawl(lastnum, id1, id2)
        else:
                print ("done")
                print (url)

        return len(arrayShopName)

#Performs crawl when shop details takes up more than 8 pages
def crawl(lastnum, id1, id2):

        last = lastnum + 7 

        for x in range (lastnum, last):
                url = "http://www.streetdirectory.com/asia_travel/travel/travel_id_" + str(id1) + "/travel_site_" + str(id2) + "/overview/page-"+ str(x) +".html"
                page = urllib.request.urlopen(url)
                soup = BeautifulSoup(page.read(),"html.parser")
                mall = soup.findAll("a", {"class": "listing_company_name"})
                category = soup.findAll("div", {"class": "Link21"}) 
                unit = soup.findAll("div",text = re.compile("Unit"))

                for all in mall:
                    text = all.get_text()
                    arrayShopName.append(text.encode('utf-8'))                                                     

                for item in unit:
                    UnitTag = item.get_text()
                    unitRegex = (re.split(': |,', UnitTag ))
                    arrayUnitNum.append(unitRegex)

                for item in category:
                    CatTag = item.get_text()
                    CatRegex = (re.split(': ', CatTag))
                    arrayCategory.append(CatRegex)
        
        checkpage(url, last, id1, id2)

#check for the validity of mall crawl request
def checkPageResponse(ret_data):
        br = mechanicalsoup.StatefulBrowser()
        web = "http://www.streetdirectory.com/"
        response = br.open(web)
        br.select_form('#fSdSearch')
        br['q']=str(ret_data)
        br.submit_selected()
        link = urlparse(br.get_url())
        if(link.path=='/asia_travel/search/'):
            return "error"
        else:
            return link

#Webcrawl and storage of shop detail into database
def CrawlMallFromWeb(ret_data, ret_addr, ret_postal, link):

        conn =pymysql.connect(host='localhost',
                                       database='navimalldb',
                                       user='admin',
                                       password='adminAccept')
  
        c = conn.cursor()

        c.execute("INSERT INTO mall(MallName, Address, PostalCode) VALUES(%s,%s,%s)",(ret_data, ret_addr, ret_postal))
        conn.commit()

        c.execute("SELECT MallID FROM mall WHERE MallName = %s", ret_data)
        MallID = c.fetchone() 
               
        subdir = link.path.split('/')[4:]
        unlist = ''.join(subdir)

        for x in range(firstnum, lastnum): 
                id = unlist.split(".", 1)[0]                 
                id1 = id.split("_", 1)[0]                   
                id2 = id.split("_", 1)[1]                   

                website =  "http://www.streetdirectory.com/asia_travel/travel/travel_id_" + str(id1) + "/travel_site_" + str(id2) + "/overview/page-"+ str(x) +".html" #URL of individual pages
                page = urllib.request.urlopen(website)                                                              
                soup = BeautifulSoup(page.read(),"html.parser")                                                     
                mall = soup.findAll("a", {"class": "listing_company_name"})                                         
                category = soup.findAll("div", {"class": "Link21"}) 
                unit = soup.findAll("div",text = re.compile("Unit"))                                                                                                    

                for shopitem in mall:
                    text = shopitem.get_text()
                    arrayShopName.append(text.encode('utf-8'))                                                      

                for unititem in unit:
                    UnitTag = unititem.get_text()
                    unitRegex = (re.split(': |,', UnitTag ))
                    arrayUnitNum.append(unitRegex)

                for catitem in category:
                    CatTag = catitem.get_text()
                    CatRegex = (re.split(': ', CatTag))
                    arrayCategory.append(CatRegex)
                                                                                                
        
        NumOfResult= checkpage(website, lastnum, id1, id2)                                           
                                                                                                     
        index = 0

        while index < NumOfResult:
            c.execute("INSERT INTO shop(UnitNum, ShopName, Category, MallID) VALUES(%s,%s,%s,%s)",(arrayUnitNum[index][1], arrayShopName[index].decode('utf-8'), arrayCategory[index][1], MallID[0]))
            conn.commit()
            index = index + 1
        
        arrayShopName.clear()                                                                                       
        arrayUnitNum.clear()
        arrayCategory.clear()               

        c.close()
        conn.close()
        recategorize()

