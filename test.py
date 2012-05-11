#-*-coding:UTF-8-*-  
'''
Created on 2012-2-7

@author: Administrator
'''
import cgi
import os
import datetime
from datetime import tzinfo,timedelta
import time
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

# 课程实体
class Course(db.Model):
    name = db.StringProperty(required=True)
    #user = db.User.Property()
    #location = db.GeoPtProperty(required=True)
    #building = db.IntegerProperty()
    classroom  = db.StringProperty(required=True)
    start_date = db.DateProperty(required=True)
    end_date = db.DateProperty(required=True)
    start_time = db.IntegerProperty()
    end_time = db.IntegerProperty()
    
class UTC(tzinfo):  
        def __init__(self,offset = 0):        
            self._offset = offset    
        def utcoffset(self, dt):        
            return timedelta(hours=self._offset)
             
        def tzname(self, dt):        
            return "UTC +%s" % self._offset
             
        def dst(self, dt):        
            return timedelta(hours=self._offset)
            
# 请求处理器
class MainPage(webapp.RequestHandler):
    def get(self):
        server_time  = datetime.datetime.now(None)
        china_time = datetime.datetime.now(UTC(8))
        
        self.response.out.write("服务器时间: %s,中国时间: %s" % (server_time, china_time))
        
# 定义了一个应用程序 ,由MainPage处理器处理/test请求的,就算app.yaml里注明了/test也必须写出来...
application = webapp.WSGIApplication([('/test',MainPage),],debug = True) 
        
def main():
    # 运行程序
    #print 'test'
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    