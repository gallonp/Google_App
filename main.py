import os
##from string import letters
##from google.appengine.ext import db

import webapp2
import re
import jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
##
##uname=''
##
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validName(username):
    return username and USER_RE.match(username)
    
PASSWORD_RE = re.compile(r"^.{3,20}$")
def validPassword(password):
    return password and PASSWORD_RE.match(password)

    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validEmail(email):
    return not email or EMAIL_RE.match(email)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

  
class welcomeHandler(BaseHandler):
    def get(self):
        username=self.request.get('username')
        self.render('welcome.html',username=username)
        
        
        
class MainHandler(BaseHandler):
    
    def valid_username(self,username):
        if  validName(username):
            return ''
        else:
            return "That's not a valid username."

    def valid_password(self,password):
        if  validPassword(password):
            return ''
        else:
            return "That wasn't a valid password"
        
    def valid_email(self,email):
        if  email and not validEmail(email):
            return  "That's not a valid email addres"
        else:
            return ''
        
    def checkPasswordMatch(self,firstPassword,secondPassword):
        if firstPassword in secondPassword and secondPassword in firstPassword:
            return ''
        else:
            return "Your passwords didn't match"
        
##    def write_form(self,username="",email="",userNameError="",passwordInvalidError="",passwordNotMatchError="",emailInvalidError=""):
##        self.response.write(form %{"username":username,
##                                   "email":email,
##                                   "userNameError":userNameError,
##                                   "passwordInvalidError":passwordInvalidError,
##                                   "passwordNotMatchError":passwordNotMatchError,
##                                   "emailInvalidError":emailInvalidError})
    def get(self):
        self.render("mainpage.html")
        
    def post(self):
        global uname
        username=self.request.get('username')
        userNameError=self.valid_username(username)
        password=self.request.get('password')
        passwordInvalidError=self.valid_password(password)
        passwordNotMatchError=''
        if passwordInvalidError =='':
            varify=self.request.get('verify')
            passwordNotMatchError=self.checkPasswordMatch(password,varify)
        email=self.request.get('email')
        emailInvalidError=self.valid_email(email)
        
        params = dict(username = username,
                      email = email)

        
        if (userNameError =='' and passwordInvalidError =='' and passwordNotMatchError =='' and emailInvalidError ==''):
            uname=username
            self.redirect("/welcome?username="+username)
        else:
            params['error_username'] =userNameError
            params['error_password'] =passwordInvalidError
            params['error_verify'] =passwordNotMatchError
            params['error_email'] =emailInvalidError
            self.render('mainpage.html', **params)
##            self.write_form(username,email,userNameError,passwordInvalidError,passwordNotMatchError,emailInvalidError)      
##        self.response.out.write(pswrd)
##        self.response.out.write(vrfy)

class SettingsHandler(BaseHandler):
    def get(self):
##        nam=self.resquest.get('page')
        self.response.write('nam')



app = webapp2.WSGIApplication([('/', MainHandler),('/welcome',welcomeHandler),('/wiki', SettingsHandler,'ust')], debug=True)


##import webapp2
##import cgi
##form="""
##<h2>Unit 2 Rot 13</h2>
##
##<form method="post">
##      <textarea name="text"
##                style="height: 100px; width: 400px;">%s</textarea>
##      <br>
##      <input type="submit">
##    </form>
##    """
##def escapehtml(s):
##    return cgi.escape(s,quote=True)
##
##def rot13(s):
##    
##    chars = "abcdefghijklmnopqrstuvwxyz"
##    Chars=chars.upper()
##    trans = chars[13:]+chars[:13]
##    Trans= Chars[13:]+Chars[:13]
##    d=dict();
##    for t in trans :
##        d[t]=chars[trans.find(t)]
##    for T in Trans:
##         d[T]=Chars[Trans.find(T)]
####    print(d[s])
##    if s in chars or s in Chars:
##        return d[s]
##    else:
##        return s
##
##    
##def stringRot13(s):
##    out=list()
####    print out
##    for each in s:
####        print(each)
####        print rot13(each)
##        out.append(rot13(each))
##    return ''.join(out)
####    print ''.join(out)
##
##    
##
##class MainHandler(webapp2.RequestHandler):
##    def write_form(self,text=""):
##        self.response.write(form%text)
##    def get(self):
##        self.write_form()
##    def post(self):
##        self.write_form(escapehtml(stringRot13(self.request.get('text'))))
##
##
##app = webapp2.WSGIApplication([
##    ('/', MainHandler)], debug=True)
##
##
##
##
##
##
##
##
##
##
##
##
##
#####!/usr/bin/env python
#####
##### Copyright 2007 Google Inc.
#####
##### Licensed under the Apache License, Version 2.0 (the "License");
##### you may not use this file except in compliance with the License.
##### You may obtain a copy of the License at
#####
#####     http://www.apache.org/licenses/LICENSE-2.0
#####
##### Unless required by applicable law or agreed to in writing, software
##### distributed under the License is distributed on an "AS IS" BASIS,
##### WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##### See the License for the specific language governing permissions and
##### limitations under the License.
##### method="post" action="/testform"
######form="""
######<form action="/testform" >
######    <label>
######        one
######        <input type="radio" value="1" name="q">
######    </label>
######    <label>
######        two
######        <input type="radio" value="2" name="q">
######    </label>    <label>
######        three
######        <input type="radio" value="3" name="q">
######    </label>
######    <select name="q">
######        <option value="1">one</option>
######        <option value="2">two</option>
######        <option value="3">three</option>
######        </select>
######    <br>
######    <input type="submit">
######</form>
######"""
######import webapp2
######
######class MainHandler(webapp2.RequestHandler):
######    def get(self):
######        self.response.write(form)
######
######class TestHandler(webapp2.RequestHandler):
######    def get(self):
######        q=self.request.get("q")
######        self.response.out.write(q)
######        
######        #self.response.headers['content-Type']='text/plain'
######        #self.response.out.write(self.request)
######
######app = webapp2.WSGIApplication([
######    ('/', MainHandler),('/testform',TestHandler)
######], debug=True)
####


####
####months = ['January','February', 'March','April','May','June','July', 'August', 'September','October', 'November', 'December']
####
####month_abbvs=dict((m[:3].lower(),m) for m in months)
####
####def valid_month(month):
####    if month:
####        short_month=month[:3].lower()
####        return month_abbvs.get(short_month)
####
####
####    
####def valid_day(day):
####    if day and day.isdigit():
####        day=int(day)
####        if day>0 and day<32:
####            return day
####    return None       
####
####
####def valid_year(year):
####    if year and year.isdigit():
####        year=int(year)
####        if 1900<=year <=2020:
####            return year
####    return None
####
####def escapehtml(s):
####    return cgi.escape(s,quote=True)
######        s=s.replace("&","&amp;")
######        s=s.replace(">","&gt;")
######        s=s.replace("<","&lt;")
######        s=s.replace('"',"&quot;")
####
####
####form="""
####<form method="post" >
####    What is your birthday?
####    <br>
####    <label>month<input type="text" value="%(month)s" name="month"></label>
####    <label>day<input type="text" value="%(day)s" name="day"></label>
####    <label>year<input type="text" value="%(year)s" name="year"></label>
####    <div style="color:red">%(error)s</div>
####    <br>
####    <input type="submit">
####</form>
####"""
####import webapp2
####import cgi
####
####class MainHandler(webapp2.RequestHandler):
####
####
####        
####    
####    def write_form(self,error="",month="",day="",year=""):     
####        self.response.out.write(form %{"error":error,
####                                       "month":escapehtml(month),
####                                       "day": escapehtml(day),
####                                       "year": escapehtml(year)})
####
####
####
##### > with &gt;
##### < with &lt;
##### " with &quot;
##### & with &amp;
####   
####                                
####    def get(self):
####        self.write_form()
####        
####    def post(self):
####        input_month=self.request.get('month')
####        input_day=self.request.get('day')
####        input_year=self.request.get('year')
####
####        month=valid_month(input_month)
####        day=valid_day(input_day)
####        year=valid_year(input_year)
####        if month and day and year:
######            self.response.out.write("Thanks! Tha's a totally valid day!")
####            self.redirect("/thanks")
####        else:
####            self.write_form("not a right date",input_month,input_day,input_year)
####
####
####class ThanksHandler(webapp2.RequestHandler):
####    def get(self):
####        self.response.out.write("Thanks!")
####
####
####app = webapp2.WSGIApplication([
####    ('/', MainHandler),('/thanks',ThanksHandler)], debug=True)




