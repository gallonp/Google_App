import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if USER_RE.match(username):
         return username
    else:
        return "error"

print(valid_username("gakfkluyf1425..."))
