#-*-coding:UTF-8-*-  

import cgi
import os
import datetime
import time
from datetime import tzinfo,timedelta,date
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import users

# 教学楼实体
class Building(db.Model):
    buildingname = db.StringProperty()
    x = db.FloatProperty()
    y = db.FloatProperty()

# 课程实体
class Course(db.Model):
    coursename = db.StringProperty()
    building = db.ReferenceProperty(Building)       # 外键
    classroom  = db.StringProperty()
    start_date = db.DateProperty()
    end_date = db.DateProperty()
    start_time = db.IntegerProperty()
    end_time = db.IntegerProperty()

# 课表实体
class Schedule(db.Model):
    user = db.UserProperty()
    course = db.ReferenceProperty(Course)           # 外键

# 时区处理
class UTC(tzinfo):  
        def __init__(self,offset = 0):        
            self._offset = offset    
        def utcoffset(self, dt):        
            return timedelta(hours=self._offset)
        def tzname(self, dt):        
            return "UTC +%s" % self._offset
        def dst(self, dt):        
            return timedelta(hours=self._offset)

# 日期转换
def StrToDate(str):
    t = time.strptime(str, "%Y-%M-%d")
    y,m,d = t[0:3]
    return date(y,m,d)

# 用户是否登录,返回(url,url_text)
def IsLogin(self):
    if users.get_current_user():
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'
    else:
        url = users.create_login_url(self.request.uri)
        url_linktext = 'Login'
    return (url,url_linktext)

# 用户是否是管理员
def IsAdmin(self):
    if users.is_current_user_admin():
        return True
    else:
        return False
    
class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

# 请求处理器
class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        url,url_linktext = IsLogin(self)
        #=======================================================================
        # if users.get_current_user():
        #    url = users.create_logout_url(self.request.uri)
        #    url_linktext = 'Logout'
        # else:
        #    url = users.create_login_url(self.request.uri)
        #    url_linktext = 'Login'
        #=======================================================================

        #courses = Course.all()
        schedule = Schedule.all()
        user = users.get_current_user()
        sel =  schedule.filter('user', user)
   
        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            'schedule': sel,
            'user': user
        }
        
        path = os.path.join(os.path.dirname(__file__), 'template_demo.html')
        self.response.out.write(template.render(path, template_values))

# 定义了一个应用程序 ,由MainPage处理器处理根目录请求的
application = webapp.WSGIApplication(
                                     [('/template',MainPage),                                     
                                      ],
                                       debug = True
                                     ) 
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    

