#-*-coding:UTF-8-*-  
'''
Created on 2012-2-7

@author: kwdhd
'''
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

#.........................自定义类型...................................
# 教学楼实体
class Building(db.Model):
    buildingname = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()

# 课程实体
class Course(db.Model):
    coursename = db.StringProperty()
    building = db.ReferenceProperty(Building)       # 外键
    classroom  = db.StringProperty()
    start_week = db.IntegerProperty()
    end_week = db.IntegerProperty()
    start_time = db.IntegerProperty()
    end_time = db.IntegerProperty()
    weekdays = db.IntegerProperty()

# 课表实体
class Schedule(db.Model):
    user = db.UserProperty()
    course = db.ReferenceProperty(Course)           # 外键

# 作息时间表
class TimeTabling(db.Model):
    ix = db.IntegerProperty()
    time = db.StringProperty()
    
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
        
#......................自定义函数...........................
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

# .....................请求处理器........................................
class MainPage(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        # 读出所有课程
        courses = Course.all()
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'courses': courses
        }
        path = os.path.join(os.path.dirname(__file__), 'Main.html')
        self.response.out.write(template.render(path, template_values))

# 添加教学楼
class AddBuilding(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        isadmin = IsAdmin(self)
        if not isadmin:
            self.response.out.write('''<script  type="text/javascript">alert('只有管理员可以添加教学楼!');
                                window.location= '/course';
            </script>''')
        # 输出所有教学楼
        buildings = db.Query(Building)
        count = buildings.count()
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'isadmin': isadmin,
            'buildings': buildings,
            'count': count
        }
        path = os.path.join(os.path.dirname(__file__), 'AddBuilding.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            building = Building()
            building.buildingname = self.request.get('name')
            building.lat = float(self.request.get('lat'))
            building.lng = float(self.request.get('lng'))
            building.put()
            self.response.out.write('''<script  type="text/javascript">alert('添加成功!');
            window.location= '/course/AddBuilding';
            </script>''')
            #self.redirect('/course/AddBuilding')
        except( TypeError, ValueError):
            self.response.out.write('''<script  type="text/javascript">alert('添加失败!');
            window.location= '/course/AddBuilding';
            </script>''')
    
# 添加课程
class AddCourse(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        isadmin = IsAdmin(self)
        if not isadmin:
            self.response.out.write('''<script  type="text/javascript">alert('只有管理员可以添加教学楼!');
                                window.location= '/course';
            </script>''')
        # 读出课程
        # 读出所有教学楼供选择...
        courses = Course.all()
        buildings = Building.all()
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'isadmin': isadmin,
            'buildings': buildings,
            'courses': courses
        }
        path = os.path.join(os.path.dirname(__file__), 'AddCourse.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        try:
            course = Course()
            course.coursename = self.request.get('name')
            course.building = Building.get(self.request.get('building'))
            course.classroom = self.request.get('classroom')
            course.start_week = int(self.request.get('start_week'))
            course.end_week = int(self.request.get('end_week'))
            course.start_time = int(self.request.get('start_time'))
            course.end_time = int(self.request.get('end_time'))
            course.weekdays = int(self.request.get('weekdays'))
            course.put()
            self.response.out.write('''<script  type="text/javascript">alert('添加成功!');
            window.location= '/course/AddCourse';
            </script>''')
            #self.response.out.write('添加成功...')
            self.redirect('/course/AddCourse')
        except( TypeError, ValueError):
            self.response.out.write('''<script  type="text/javascript">alert('添加失败!');
            window.location= '/course/AddCourse';
            </script>''')
#            self.response.out.write("fail!" )

# 添加课程表
class AddSchedule(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        isadmin = IsAdmin(self)
        if not user:
            self.response.out.write('''<script  type="text/javascript">alert('请登陆之后再添加课程表!');
                                window.location= '/course';
            </script>''')
        # 显示所有课程
        courses = Course.all()
        schedule = Schedule.all()
        sel =  schedule.filter('user', user)
        selected = []
        if courses.count() != 0:
            for c in courses:
                # 判断当前用户是否已选择这门课,构造列表
                count = 0
                for s in sel:
                    if s.course.key() == c.key(): 
                        count = count +1
                        break
                if count == 0:
                    # 没有选这门课
                    selected.append((''' ''',c))
                else:
                    selected.append(('''checked="checked"''',c))
        # 课程数
        count = courses.count()          
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'isadmin': isadmin,
            'selected': selected,
            'count': count
        }
        path = os.path.join(os.path.dirname(__file__), 'AddSchedule.html')
        self.response.out.write(template.render(path, template_values))
                               
    def post(self):
        try:
            user = users.get_current_user()
            # selected,用户已选择的课
            selected = db.Query(Schedule).filter('user',user)            
            courses = self.request.get("courses",allow_multiple=True) # get Course key
            # 新选中的课 new
            new = Course()  
            for c in courses:
                # 如果之前没有选,添加到数据库中
                count = 0
                for s in selected:
                # 判断当前用户是否已选择这门课
                    # ????? 直接比较key或对象值永远是false ?????
                    #self.response.out.write('''s.course.key(): %s  ==  c: %s  = %s</br>'''%(s.course.key(),c,s.course.coursename == Course.get(c).coursename))
                    if s.course.coursename == Course.get(c).coursename: 
                        count = count +1
                        break
                # 如果没有选择,添加到数据库
                if count == 0:
                    new = Schedule()
                    new.user = user
                    new.course = Course.get(c)
                    new.put()
            # 从课程表中删除被取消的课程
            for s in selected:
                count = 0
                for c in courses:
                    if s.course.coursename == Course.get(c).coursename: 
                        count = count +1
                        break
                if count == 0:
                    db.delete(s)   
            self.response.out.write('''<script  type="text/javascript">alert('修改成功!');
            window.location= '/course/AddSchedule';
            </script>''')
        except( TypeError, ValueError):
            self.response.out.write('''<script  type="text/javascript">alert('修改失败!');
            window.location= '/course/AddSchedule';
            </script>''')
            #self.response.out.write("fail!" )

# 显示用户建立的课程表..
class MySchedule(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        if not user:
            self.response.out.write('''<script  type="text/javascript">alert('请先登陆!');
                                window.location= '/course';
            </script>''')
        # 读出所有课程
        selected = db.Query(Schedule).filter('user',user)
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'selected': selected
        }
        path = os.path.join(os.path.dirname(__file__), 'MySchedule.html')
        self.response.out.write(template.render(path, template_values))

class TimeTable(webapp.RequestHandler):
    def get(self):
        # 用户登录,判断
        user = users.get_current_user()
        url,url_linktext = IsLogin(self)
        isadmin = IsAdmin(self)
        if not isadmin:
            self.response.out.write('''<script  type="text/javascript">alert('只有管理员可以添加教学楼!');
                                window.location= '/course';
            </script>''')
        # 读出所有课程
        timetable = db.Query(TimeTabling)
        # 固定部分,输出内容到模板...
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'timetable': timetable
        }
        path = os.path.join(os.path.dirname(__file__), 'timetabling.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        try:
            newtime = TimeTabling()
            newtime.ix = int(self.request.get('ix'))
            # self.response.out.write('''<script  type="text/javascript">alert('%s');</script>'''%self.request.get('ix'))
            newtime.time = self.request.get('time')
            newtime.put()
            self.response.out.write('''<script  type="text/javascript">alert('添加成功!');window.location= '/course/TimeTable';</script>''')
        except( TypeError, ValueError):
            self.response.out.write('''<script  type="text/javascript">alert('添加失败!'); window.location= '/course/TimeTabling'; </script>''')

#.................................................................................................
# 定义了一个应用程序 ,由MainPage处理器处理根目录请求的
application = webapp.WSGIApplication(
                                     [('/course',MainPage),
                                      ('/course/AddBuilding',AddBuilding),
                                      ('/course/AddCourse',AddCourse),
                                      ('/course/AddSchedule',AddSchedule),
                                      ('/course/MySchedule',MySchedule),
                                      ('/course/TimeTable',TimeTable)                                      
                                      ],
                                       debug = True
                                     ) 
        
def main():
    # 运行程序
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    

