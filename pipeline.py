import sys
from twisted.enterprise import adbapi    
from scrapy.utils.project import get_project_settings 
import hashlib
from scrapy import log
import MySQLdb
from scrapy.exceptions import DropItem
from scrapy.http import Request

settings = get_project_settings()


class ZillowSamplePipeline(object):    
 
    def __init__(self):    
        dbargs = settings.get('DB_CONNECT')    
        db_server = settings.get('DB_SERVER')    
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)    
        self.dbpool = dbpool 
 
    def __del__(self):    
        self.dbpool.close()    
 
    def process_item(self, item, spider):
    	query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)    
        return item    
 
    def _conditional_insert(self, tx, item):
    	#doesnt allow duplicates.
    	tx.execute("select * from test where date = %s and title =%s", (item['date'], item['title'] ))
        result = tx.fetchone()
        if result:
            log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
        else:
        #insert data
            tx.execute(\
                "insert into test (title, number, date) "
                "values (%s, %s, %s)",
                (item['title'],
                 item['number'],
                 item['date']))
            log.msg("Item stored in db: %s" % item, level=log.DEBUG)
            #re-organize data  
            tx.execute("SELECT * FROM test ORDER BY title")
           	
            
    def handle_error(self, e):
        log.err(e)
