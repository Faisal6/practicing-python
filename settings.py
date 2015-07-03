# -*- coding: utf-8 -*-

# Scrapy settings for zillow_sample project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zillow_sample'

SPIDER_MODULES = ['zillow_sample.spiders']
NEWSPIDER_MODULE = 'zillow_sample.spiders'
ITEM_PIPELINES = {
    'zillow_sample.pipelines.ZillowSamplePipeline': 100,
}

DB_SERVER = 'MySQLdb'            # For detail, please see twisted doc
DB_CONNECT = {    
    'db': 'new',             # Your db   
    'user': 'root',              # 
    'passwd': 'apple',            # 
    'host': '127.0.0.1',      # Your Server
    'charset': 'utf8',    
    'use_unicode': True,    
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zillow_sample (+http://www.yourdomain.com)'
