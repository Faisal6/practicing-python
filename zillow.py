import time
import mypkg
import re
import string
from selenium import webdriver
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import signals
from scrapy.http import TextResponse 
from scrapy.xlib.pydispatch import dispatcher
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from zillow_sample.items import ZillowSampleItem
from urlparse import urlparse
import mysql.connector

class MySpider(BaseSpider):
    name = "num"
    allowed_domains = ["zillow.com"]
    start_urls = [
    "http://www.zillow.com/homes/for_sale/New-York-NY/6181_rid/49.239121,-55.546875,33.760882,-118.564453_rect/3_zm/1_fr/", 
    "http://www.zillow.com/homes/Los-Angeles-CA_rb/",
    "http://www.zillow.com/homes/miami_rb/",
    "http://www.zillow.com/homes/chicago_rb/"
    ]
    
    def __init__(self):
    	self.driver = webdriver.Firefox()
    	self.driver.implicitly_wait(10)
    	
    		
    def parse(self, response):
    	delay = 10
    	try:
    		self.driver.get(response.url)
    		WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, 'map-result-count-message')))
    	except:
    		print "page is not ready!"
    	 
        numbers = self.driver.find_elements_by_xpath("/html")
        items = []
        for numbers in numbers:
        	item = ZillowSampleItem()
        	name = str((response.xpath("/html/head/title/text()")))
        	splitted = name.split()
        	newstr = str(re.sub("data=u'","",name,count=1))
        	newstr1 = str(re.sub("Real",".",newstr,count=1))
        	splitted2 = newstr1.split()
        	item ['date'] = (time.strftime("%m/%d/%Y"))
        	item ['title'] = splitted2[2:5]
        	title = str((response.xpath("/html/head/title/text()")))
        	item ['number'] = (re.findall('\d+', title ))
        	items.append(item)
        return items
