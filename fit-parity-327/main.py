import os
import webapp2
import re
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class blogPost(db.Model):
    title=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    



class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_front(self, template,kw):
        blogs=db.GqlQuery("SELECT * FROM blogPost ORDER BY created DESC")
        kw['blogs']=blogs
        self.render(template,**kw)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class blogPageHandler(BaseHandler):

    def get(self):
        self.render('Blogmainpage.html')
    def post(self):
        Title=self.request.get('title')
        content=self.request.get('content')
        params=dict(tle=Title,blogContent=content)
        has_title=True
        has_content=True
        if  Title =='':
            has_title=False
            params['error_title']='Must have a title'
        if  content =='':
            has_content=False
            params['error_content']='Must have  content'          
            
        if has_title and has_content:
            #self.render('Bolgmainpage.html',**params)#connect to db and store
            a=blogPost(title=Title,content=content)
            a.put()
            postID=a.key().id()
            self.redirect('/blog/'+str(postID))
##            self.render('Blogmainpage.html',**params)
##        self.render_front('Blogmainpage.html',params)


class frontPageHandler(BaseHandler):
    def get(self):
        params=dict()
        self.render_front('front.html',params)

class newpostHandler(BaseHandler):
    def get(self,page):
##        params=dict()
##        self.render_front('front.html',params)
        post=blogPost.get_by_id(long(page))
        params=dict(blog=post)
        self.render('newpost.html',**params)
        
        
app = webapp2.WSGIApplication([('/blog', frontPageHandler),
                               ('/blog/newpost',blogPageHandler),
                               webapp2.Route('/blog/<page>', handler=newpostHandler, name='newpost')],
                              debug=True)

        
























##form="""
##<head>
##    <title>Sign Up</title>
##    <style type="text/css">
##      .label {text-align: right}
##      .error {color: red}
##    </style>
##
##  </head>
##
##  <body>
##    <h2>Signup</h2>
##    <form method="post">
##      <table>
##        <tr>
##          <td class="label">
##            Username
##          </td>
##          <td>
##            <input type="text" name="username" value="%(username)s">
##          </td>
##          <td class="error">
##            %(userNameError)s
##          </td>
##        </tr>
##
##        <tr>
##          <td class="label">
##            Password
##          </td>
##          <td>
##            <input type="password" name="password" value="">
##          </td>
##          <td class="error">
##            %(passwordInvalidError)s
##          </td>
##        </tr>
##
##        <tr>
##          <td class="label">
##            Verify Password
##          </td>
##          <td>
##            <input type="password" name="verify" value="">
##          </td>
##          <td class="error">
##               %(passwordNotMatchError)s
##          </td>
##        </tr>
##
##        <tr>
##          <td class="label">
##            Email (optional)
##          </td>
##          <td>
##            <input type="text" name="email" value="%(email)s">
##          </td>
##          <td class="error">
##                %(emailInvalidError)s
##          </td>
##        </tr>
##      </table>
##
##      <input type="submit">
##    </form>
##  </body>
##  """
##welcomePage="""
##    <title>Unit 2 Signup</title>
##  </head>
##
##  <body>
##    <h2>Welcome, %s!</h2>
##  </body>
##
##"""
##
##import webapp2
##import re
##
##uname=''
##
##USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
##def validName(username):
##    if USER_RE.match(username):
##        return True
##    else:
##        return False
##    
##PASSWORD_RE = re.compile(r"^.{3,20}$")
##def validPassword(password):
##    if PASSWORD_RE.match(password):
##        return True
##    else:
##        return False
##    
##EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
##def validEmail(email):
##    if EMAIL_RE.match(email):
##        return True
##    else:
##        return False   
##
##
##class welcomeHandler(webapp2.RequestHandler):
##    def get(self):
##        global uname
##        self.response.out.write(welcomePage%uname)
##
##class MainHandler(webapp2.RequestHandler):
##    
##    def valid_username(self,username):
##        if  validName(username):
##            return ''
##        else:
##            return "That's not a valid username."
##
##    def valid_password(self,password):
##        if  validPassword(password):
##            return ''
##        else:
##            return "That wasn't a valid password"
##        
##    def valid_email(self,email):
##        if  email and not validEmail(email):
##            return  "That's not a valid email addres"
##        else:
##            return ''
##        
##        
##    def checkPasswordMatch(self,firstPassword,secondPassword):
##        if firstPassword in secondPassword and secondPassword in firstPassword:
##            return ''
##        else:
##            return "Your passwords didn't match"
##        
##
##        
##    def write_form(self,username="",email="",userNameError="",passwordInvalidError="",passwordNotMatchError="",emailInvalidError=""):
##        self.response.write(form %{"username":username,
##                                   "email":email,
##                                   "userNameError":userNameError,
##                                   "passwordInvalidError":passwordInvalidError,
##                                   "passwordNotMatchError":passwordNotMatchError,
##                                   "emailInvalidError":emailInvalidError})
##    def get(self):
##        self.write_form()
##        
##    def post(self):
##        global uname
##        username=self.request.get('username')
##        userNameError=self.valid_username(username)
##        password=self.request.get('password')
##        passwordInvalidError=self.valid_password(password)
##        passwordNotMatchError=''
##        if passwordInvalidError =='':
##            varify=self.request.get('verify')
##            passwordNotMatchError=self.checkPasswordMatch(password,varify)
##        email=self.request.get('email')
##        emailInvalidError=self.valid_email(email)
##        if (userNameError =='' and passwordInvalidError =='' and passwordNotMatchError =='' and emailInvalidError ==''):
##            uname=username
##            self.redirect("/welcome")
##        else:
####            self.response.out.write('not good')
##            self.write_form(username,email,userNameError,passwordInvalidError,passwordNotMatchError,emailInvalidError)      
####        self.response.out.write(pswrd)
####        self.response.out.write(vrfy)
##
##
##app = webapp2.WSGIApplication([
##    ('/', MainHandler),('/welcome',welcomeHandler)], debug=True)
##
##
####import webapp2
####import cgi
####form="""
####<h2>Unit 2 Rot 13</h2>
####
####<form method="post">
####      <textarea name="text"
####                style="height: 100px; width: 400px;">%s</textarea>
####      <br>
####      <input type="submit">
####    </form>
####    """
####def escapehtml(s):
####    return cgi.escape(s,quote=True)
####
####def rot13(s):
####    
####    chars = "abcdefghijklmnopqrstuvwxyz"
####    Chars=chars.upper()
####    trans = chars[13:]+chars[:13]
####    Trans= Chars[13:]+Chars[:13]
####    d=dict();
####    for t in trans :
####        d[t]=chars[trans.find(t)]
####    for T in Trans:
####         d[T]=Chars[Trans.find(T)]
######    print(d[s])
####    if s in chars or s in Chars:
####        return d[s]
####    else:
####        return s
####
####    
####def stringRot13(s):
####    out=list()
######    print out
####    for each in s:
######        print(each)
######        print rot13(each)
####        out.append(rot13(each))
####    return ''.join(out)
######    print ''.join(out)
####
####    
####
####class MainHandler(webapp2.RequestHandler):
####    def write_form(self,text=""):
####        self.response.write(form%text)
####    def get(self):
####        self.write_form()
####    def post(self):
####        self.write_form(escapehtml(stringRot13(self.request.get('text'))))
####
####
####app = webapp2.WSGIApplication([
####    ('/', MainHandler)], debug=True)
####
####
####
####
####
####
####
####
####
####
####
####
####
#######!/usr/bin/env python
#######
####### Copyright 2007 Google Inc.
#######
####### Licensed under the Apache License, Version 2.0 (the "License");
####### you may not use this file except in compliance with the License.
####### You may obtain a copy of the License at
#######
#######     http://www.apache.org/licenses/LICENSE-2.0
#######
####### Unless required by applicable law or agreed to in writing, software
####### distributed under the License is distributed on an "AS IS" BASIS,
####### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
####### See the License for the specific language governing permissions and
####### limitations under the License.
####### method="post" action="/testform"
########form="""
########<form action="/testform" >
########    <label>
########        one
########        <input type="radio" value="1" name="q">
########    </label>
########    <label>
########        two
########        <input type="radio" value="2" name="q">
########    </label>    <label>
########        three
########        <input type="radio" value="3" name="q">
########    </label>
########    <select name="q">
########        <option value="1">one</option>
########        <option value="2">two</option>
########        <option value="3">three</option>
########        </select>
########    <br>
########    <input type="submit">
########</form>
########"""
########import webapp2
########
########class MainHandler(webapp2.RequestHandler):
########    def get(self):
########        self.response.write(form)
########
########class TestHandler(webapp2.RequestHandler):
########    def get(self):
########        q=self.request.get("q")
########        self.response.out.write(q)
########        
########        #self.response.headers['content-Type']='text/plain'
########        #self.response.out.write(self.request)
########
########app = webapp2.WSGIApplication([
########    ('/', MainHandler),('/testform',TestHandler)
########], debug=True)
######
######
######
######
######months = ['January','February', 'March','April','May','June','July', 'August', 'September','October', 'November', 'December']
######
######month_abbvs=dict((m[:3].lower(),m) for m in months)
######
######def valid_month(month):
######    if month:
######        short_month=month[:3].lower()
######        return month_abbvs.get(short_month)
######
######
######    
######def valid_day(day):
######    if day and day.isdigit():
######        day=int(day)
######        if day>0 and day<32:
######            return day
######    return None       
######
######
######def valid_year(year):
######    if year and year.isdigit():
######        year=int(year)
######        if 1900<=year <=2020:
######            return year
######    return None
######
######def escapehtml(s):
######    return cgi.escape(s,quote=True)
########        s=s.replace("&","&amp;")
########        s=s.replace(">","&gt;")
########        s=s.replace("<","&lt;")
########        s=s.replace('"',"&quot;")
######
######
######form="""
######<form method="post" >
######    What is your birthday?
######    <br>
######    <label>month<input type="text" value="%(month)s" name="month"></label>
######    <label>day<input type="text" value="%(day)s" name="day"></label>
######    <label>year<input type="text" value="%(year)s" name="year"></label>
######    <div style="color:red">%(error)s</div>
######    <br>
######    <input type="submit">
######</form>
######"""
######import webapp2
######import cgi
######
######class MainHandler(webapp2.RequestHandler):
######
######
######        
######    
######    def write_form(self,error="",month="",day="",year=""):     
######        self.response.out.write(form %{"error":error,
######                                       "month":escapehtml(month),
######                                       "day": escapehtml(day),
######                                       "year": escapehtml(year)})
######
######
######
####### > with &gt;
####### < with &lt;
####### " with &quot;
####### & with &amp;
######   
######                                
######    def get(self):
######        self.write_form()
######        
######    def post(self):
######        input_month=self.request.get('month')
######        input_day=self.request.get('day')
######        input_year=self.request.get('year')
######
######        month=valid_month(input_month)
######        day=valid_day(input_day)
######        year=valid_year(input_year)
######        if month and day and year:
########            self.response.out.write("Thanks! Tha's a totally valid day!")
######            self.redirect("/thanks")
######        else:
######            self.write_form("not a right date",input_month,input_day,input_year)
######
######
######class ThanksHandler(webapp2.RequestHandler):
######    def get(self):
######        self.response.out.write("Thanks!")
######
######
######app = webapp2.WSGIApplication([
######    ('/', MainHandler),('/thanks',ThanksHandler)], debug=True)
######
######
######
