#coding=utf-8
#!/usr/bin/env python
'''
Created on 2015年3月23日

@author: sanhe
'''

from bottle import route, get, post, request, response, run, template
# from bottle.ext.websocket import websocket
# from bottle.ext.websocket import GeventWebSocketServer

def check_login(username, password):
    if username == 'yang' and password=='123' :
        return True
    else:
        return False
@route('/hello')
def hello_again():
    if request.get_cookie("visited"):
        return "Welcome back ! Nice to see you again"
    else:
        response.set_cookie("visited","yes")
        return "Hello there! Nice to meet you"

@get('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        <form>
    '''
    
@post('/login')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

run(host='172.16.1.5', port=8080, debug = True)
