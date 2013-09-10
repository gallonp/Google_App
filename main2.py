form="""
<head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(userNameError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(passwordInvalidError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
               %(passwordNotMatchError)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
                %(emailNotvalidError)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>
  """


import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validName(username):
    if USER_RE.match(username):
        return True
    else:
        return False
    
PASSWORD_RE = re.compile(r"^.{3,20}$")
def validPassword(password):
    if PASSWORD_RE.match(password):
        return True
    else:
        return False
    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validEmail(email):
    if EMAIL_RE.match(email):
        return True
    else:
        return False   


class MainHandler(webapp2.RequestHandler):
    def valid_userName(self):
        username=self.request.get('username')
        if  validname(username):
            return True
        else
            return "That's not a valid username."

    def valid_password(self):
        password=self.request.get('password')
        if password:
            return true

        
    def write_form(self,text=""):
        self.response.write(form)
    def get(self):
        self.write_form()
    def post(self):
        self.write_form()


app = webapp2.WSGIApplication([
    ('/', MainHandler)], debug=True)



