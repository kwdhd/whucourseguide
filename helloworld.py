#-*-coding:UTF-8-*-  
'''
Created on 2012-2-7

@author: Administrator
'''
import cgi
import os
import datetime
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

# 
class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

# 请求处理器
class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        #self.response.out.write(path)
        self.response.out.write(template.render(path, template_values))
        #=======================================================================
        # 数据存储区demo
        # self.response.out.write('<html><body>')
        # # 读出所有的 留言
        # greetings = db.GqlQuery("SELECT * FROM Greeting ORDER BY date DESC")
        # 
        # # 显示读出的留言
        # for greeting in greetings:
        #    if greeting.author:
        #        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
        #    else:
        #        self.response.out.write('An anonymous person wrote:')
        #    self.response.out.write('<blockquote>%s</blockquote>' % cgi.escape(greeting.content))
        # 
        # self.response.out.write("""
        # <form action="/sign" method="post">
        #    <div><textarea name="content" rows="3" cols="60"></textarea></div>
        #    <div><input type="submit" value="book"></div>
        # </form>
        # </body>
        # </html>"""
        # )    
        #=======================================================================
        
        #=======================================================================
        # 表单示例
        # user = users.get_current_user()
        # self.response.out.write("""
        # <html>
        #    <body>
        #        <form action="/sign" method="post">
        #            <div><textarea name="content" rows="3" cols="60"></textarea></div>
        #            <div><input type="submit" value="Sign guestbook"></div>
        #        </form>
        #    </body>
        # </html>""")
        #=======================================================================
        #=======================================================================
        # 用户登陆示例
        # if user:
        #    self.response.headers['Content-Type'] = 'text/plain'
        #    self.response.out.write('Hello,' + user.nickname())
        # else:
        #    # 用户未登录时,重定向的登陆页
        #    self.redirect(users.create_login_url(self.request.uri))
        #=======================================================================
class Guestbook(webapp.RequestHandler):
    def post(self):
        greeting = Greeting()
        
        if users.get_current_user():
            greeting.author = users.get_current_user()
        
        greeting.content = self.request.get("content")
        greeting.put()
        self.redirect('/')
        #=======================================================================
        # self.response.out.write('<html><body>You wrote:<pre>')
        # self.response.out.write(cgi.escape(self.request.get('content')))
        # self.response.out.write('</pre></body></html>')
        #=======================================================================
# 接收两个整数输入
class InputTwoNumbers(webapp.RequestHandler):
    def get(self):
        # 把表单发送给/sum处理
        self.response.out.write("""
         <html>
         <body>
        <form action="/sum" method="post">
            First Num: <input type="text" name="first" />
            <br/>
            Second Num: <input type="text" name="second" />
            <br/>
            <input type="submit" value="Submit" />
            <br/>
            <input type="checkbox" name="fruit" value ="apple" >苹果<br>
            <input type="checkbox" name="fruit" value ="orange">桔子<br>
            <input type="checkbox" name="fruit" value ="mango">芒果<br>
            <select name='sel'>
                <option value='1'>1</option>
                <option value='2'>2</option>
            </select>
       </form>
         </body>
        </html>"""
        )   
# 计算两个数的和
class SumTwoNumbers(webapp.RequestHandler):
    def post(self):
        try:
            first = int(self.request.get('first'))
            second = int(self.request.get('second'))
            values = self.request.get("fruit",allow_multiple=True)
            sel = self.request.get('sel')
            self.response.out.write("%d + %d = %d<br/>" % (first, second, first + second))
            for value in values:
                self.response.out.write(value+'<br/>')
            self.response.out.write('sel: %s' % (sel,))
        except( TypeError, ValueError):
            self.response.out.write("Invalid inputs!  %s, %s" % (TypeError, ValueError))
        
        
class MyRequestHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
        <html>
          <body>
            <form action="/select" method="post">
              <p>Name: <input type="text" name="name" /></p>
              <p>Favorite foods:</p>
              <select multiple="true" name="favorite_foods">
                <option value="apples">Apples</option>
                <option value="bananas">Bananas</option>
                <option value="carrots">Carrots</option>
                <option value="durians">Durians</option>
              </select>
              <p>Birth year: <input type="text" name="birth_year" /></p>
              <br/>
              <input type="submit"/>
            </form>
          </body>
        </html>
        ''')

    def post(self):
       #self.response.out.write('test')
        name = self.request.get("name")
        favorite_foods = self.request.get_all("favorite_foods")
        birth_year = self.request.get_range("birth_year")
        #self.response.out.write(favorite_foods)
        #for food in favorite_foods:
        #    self.response.out.write(food)
        self.response.out.write("name = %s, favorite_foods = %s, birth_year = %d" % (name, favorite_foods, birth_year))
        
# 定义了一个应用程序 ,由MainPage处理器处理根目录请求的
application = webapp.WSGIApplication(
                                     [('/',MainPage),
                                     ('/sign',Guestbook),
                                     ('/input',InputTwoNumbers),
                                     ('/sum',SumTwoNumbers),
                                     ('/select',MyRequestHandler)
                                     ],
                                       debug = True
                                     ) 
        
def main():
    # 运行程序
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    

    
    
    
    
#===============================================================================
# print 'Content-Type: text/plain'
# print ''
# print 'Hello,world'
#===============================================================================