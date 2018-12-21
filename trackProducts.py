# import all the required modules viz bs4, lxml, xlwings
import re
import csv
from urllib import urlopen
from bs4 import BeautifulSoup
import sys
import warnings
import urllib2
from lxml import html
import datetime
import subprocess
import httplib
import xlwings

def access_amazon(asin, site_url):
    #all_amazon_items=[]
    item_array=[] #An array to store details of a single product.
    #response = session.get(site_url, headers=headers, verify=False) #get the response
    print "1 amazon +++++++++++++++++++++++ reading URL "  + site_url
    #https://www.amazon.in/dp/B075JLZ1GF
    am_req = ""
    am_req = urllib2.Request(site_url)
    am_req.add_header('Referer', 'http://www.python.org/')
    am_req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')
    try:
        am_response = urllib2.urlopen(am_req)
        dphtml = am_response.read()
    except httplib.IncompleteRead, e:
        am_response = e.partial
        dphtml = am_response.read()
    
    #am_response = urllib2.urlopen(site_url)
    #print am_response.info()
    
    am_response.close()
    #print "to slow down -> Get all data: " + dphtml
    prod_page_tree = html.fromstring(dphtml)
    ourPrice = 0
    savings = ""
    savingFigure = 0
    savingPercentage = 0
    productTitle = ""
    actualPrice = 0
    prodAvailable = ""
    prodAvailablility = True
    print "2 amazon ++++++++++++++++++++++++ reading xpaths"
    if prod_page_tree.xpath('//span[@id="priceblock_ourprice"]/text()'):
        ourPriceStr = prod_page_tree.xpath('//span[@id="priceblock_ourprice"]/text()')[0]
        ourPriceStr = ourPriceStr.replace("-", "")
        ourPriceStr = ourPriceStr.strip()
        ourPrice = float(ourPriceStr.replace(',',''))
    elif prod_page_tree.xpath('//span[@id="priceblock_saleprice"]/text()'):
        ourPriceStr = prod_page_tree.xpath('//span[@id="priceblock_saleprice"]/text()')[0]
        ourPriceStr = ourPriceStr.replace("-", "")
        ourPriceStr = ourPriceStr.strip()
        ourPrice = float(ourPriceStr.replace(',',''))
    if prod_page_tree.xpath('//tr[@id="regularprice_savings"]//td[@class="a-span12 a-color-price a-size-base"]/text()'):
        savings = prod_page_tree.xpath('//tr[@id="regularprice_savings"]//td[@class="a-span12 a-color-price a-size-base"]/text()')[0] # Need some processing
        savings = savings.strip().split(" ")
        savingFigureStr = savings[0]
        savingFigure = float(savingFigureStr.replace(',',''))
        try:
            savingPercentageStr = savings[1]
        except IndexError:
            savingPercentageStr = "0"
        print "amazon %%%% = " + savingPercentageStr
        savingPercentage = float(savingPercentageStr.strip('(').strip(')').strip('%'))
        print savingPercentage
        print "printed asfdasfdassdf saving percentage"
    if prod_page_tree.xpath('//span[@id="productTitle"]/text()'):
        productTitle = prod_page_tree.xpath('//span[@id="productTitle"]/text()')[0]  # Need some processing
        productTitle = re.sub("\n|\r", "", productTitle)
        productTitle = productTitle.strip()
    if prod_page_tree.xpath('//div[@id="price"]/table/tr[1]/td[2]/span[@class="a-text-strike"]/text()'):
        actualPriceStr = ""
        actualPriceStr = prod_page_tree.xpath('//div[@id="price"]/table/tr[1]/td[2]/span[@class="a-text-strike"]/text()')[1] # Need some processingproductTitle = actualPrice = actualPrice.strip()
        actualPrice = float(actualPriceStr.replace(',',''))
    if prod_page_tree.xpath('//div[@id="availability"]/span/text()'):
        prodAvailable = prod_page_tree.xpath('//div[@id="availability"]/span/text()')[0]
        prodAvailable = re.sub("\n|\r", "", prodAvailable)
        prodAvailable = prodAvailable.strip()
    if("unavailable" in prodAvailable):
        prodAvailablility = False
    if actualPrice == 0:
        actualPrice = ourPrice
    print "+++++++++++++++++++++++ preparing item_array"    
    #Extracting the price
    item_array.append("amazon")
    item_array.append(asin)
    item_array.append(productTitle)
    item_array.append(actualPrice)
    item_array.append(ourPrice) 
    item_array.append(savingFigure) 
    item_array.append(savingPercentage)
    item_array.append(prodAvailablility) 
    item_array.append(datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")) 
    #all_amazon_items.append(item_array)
    return item_array;
	
	
def access_flipkart(asin, site_url):
    item_array=[] #An array to store details of a single product.
    print "1 flipkart +++++++++++++++++++++++ reading URL "  + site_url
    
    flip_req = urllib2.Request(site_url)
    flip_req.add_header('Referer', 'http://www.python.org/')
    flip_req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36')
    try:
        flip_response = urllib2.urlopen(flip_req)
    except httplib.IncompleteRead, e:
        flip_response = e.partial
	
	
    print flip_response.info()
    dphtml = flip_response.read()
    flip_response.close()
    #print "to slow down -> Get all data: ", dphtml
    type(dphtml)
    prod_page_tree = html.fromstring(dphtml)
    ourPrice = 0
    savings = ""
    savingFigure = 0
    savingPercentage = 0
    productTitle = ""
    actualPrice = 0
    prodAvailable = True
    soldOutText = ""
	
    print "2 flipkart +++++++++++++++++++++++ reading xpaths"
	
    if prod_page_tree.xpath('//div[@class="_1vC4OE _3qQ9m1"]/text()')[0].encode('ascii', 'ignore'):
        ourPriceStr = prod_page_tree.xpath('//div[@class="_1vC4OE _3qQ9m1"]/text()')[0].encode('ascii', 'ignore')
        ourPrice = float(ourPriceStr.replace(',',''))
    if prod_page_tree.xpath('//div[@class="_3auQ3N _1POkHg"]/text()'):
        actualPriceStr = prod_page_tree.xpath('//div[@class="_3auQ3N _1POkHg"]/text()')[1]
        actualPrice = float(actualPriceStr.replace(',',''))
        if prod_page_tree.xpath('//div[@class="VGWI6T _1iCvwn"]/span/text()'):
            savingsList = prod_page_tree.xpath('//div[@class="VGWI6T _1iCvwn"]/span/text()')[0].split()
            savingPercentageStr = savingsList[0]
            savingPercentage = float(savingPercentageStr.strip('%'))
            savingFigure = actualPrice * savingPercentage/100
    else:
        actualPrice = ourPrice
    if prod_page_tree.xpath('//span[@class="_35KyD6"]/text()')[0]:
        productTitle = prod_page_tree.xpath('//span[@class="_35KyD6"]/text()')[0]
    if prod_page_tree.xpath('//div[@class="mBwvBe"]/text()'):
	    soldOutText = prod_page_tree.xpath('//div[@class="mBwvBe"]/text()')[0]
    if(soldOutText is 'Sold Out'):
        prodAvailable = False
  
    print "+++++++++++++++++++++++ preparing item_array"    
    #Extracting the price
    item_array.append("flipkart")
    item_array.append(site_url)
    item_array.append(productTitle)
    item_array.append(actualPrice)
    item_array.append(ourPrice) 
    item_array.append(savingFigure) 
    item_array.append(savingPercentage)
    item_array.append(prodAvailable) 
    item_array.append(datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S"))
    return item_array;

	
def tracking():
    #ignore warnings
    print "Tracking "
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    if "EmrData01" in subprocess.check_output("netsh wlan show interfaces"): 
        print "Network Error, quitting ... "
        quit()
    
    url_array=[] #array for urls
    asin_array=[] #array for asin numbers
    with open('D:\\3Code\\python\\PriceTracker\\asin_list.csv', 'r') as csvfile:
        asin_reader = csv.reader(csvfile)
        for row in asin_reader:
            url_array.append(row[0]) #This url list is an array containing all the urls from the excel sheet
            print "cell content: " + row[0]

    asin_array = url_array[:]

    for asin in asin_array:
        print "asin " + asin
        
#The ASIN Number will be between the dp/ and another /
#start = 'dp/'
#end = '/'
#for url in url_array:
#    asin_array.append(url[url.find(start)+len(start):url.rfind(end)]) #this array has all the asin numbers

    for asin in asin_array:
        print "processed asin " + asin
    

    #declare the header.
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
        }
    
    all_items=[] #The final 2D list containing prices and details of products, that will be converted to a consumable csv

    for asin in asin_array:
        if "flipkart" in asin:
            site_url=asin
            all_items.append(access_flipkart(asin, site_url))
            print site_url
        else:
            site_url="https://www.amazon.in/dp/"+asin #The general structure of a url
            all_items.append(access_amazon(asin, site_url))
            print site_url
    print all_items

    #Convert mmaster array to csv
    with open("D:\\3Code\\python\\PriceTracker\\new_file.csv","ab") as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(all_items)

		
'''
#ignore warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

if "EmrData01" in subprocess.check_output("netsh wlan show interfaces"): 
    print "Network Error, quitting ... "
    quit()

    
url_array=[] #array for urls
asin_array=[] #array for asin numbers
with open('asin_list1.csv', 'r') as csvfile:
    asin_reader = csv.reader(csvfile)
    for row in asin_reader:
        url_array.append(row[0]) #This url list is an array containing all the urls from the excel sheet
        print "cell content: " + row[0]

asin_array = url_array[:]

for asin in asin_array:
    print "asin " + asin
        
#The ASIN Number will be between the dp/ and another /
#start = 'dp/'
#end = '/'
#for url in url_array:
#    asin_array.append(url[url.find(start)+len(start):url.rfind(end)]) #this array has all the asin numbers

for asin in asin_array:
    print "processed asin " + asin
    

#declare the header.
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
    }
    
all_items=[] #The final 2D list containing prices and details of products, that will be converted to a consumable csv

for asin in asin_array:
    if "flipkart" in asin:
        site_url=asin
        all_items.append(access_flipkart(asin, site_url))
        print site_url
    else:
        site_url="https://www.amazon.in/dp/"+asin #The general structure of a url
        all_items.append(access_amazon(asin, site_url))
        print site_url
print all_items

#Convert mmaster array to csv
with open("new_file.csv","ab") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(all_items)

'''