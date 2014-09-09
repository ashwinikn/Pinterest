"""
6, Apr 2013

Example bottle (python) RESTful web service.

This example provides a basic setup of a RESTful service

Notes
1. example should perform better content negotiation. A solution is
   to use minerender (https://github.com/martinblech/mimerender)
"""
import json

import time
import sys
import socket
from data.storage import Storage
from data.models import User,Board,Pin
import mimerender
# bottle framework
from bottle import request, response, route, run, template

# moo
from classroom import Room

# virtual classroom implementation
room = None


def setup(base,conf_fn):
   print '\n**** service initialization ****\n'
   global room
   room = Room(base,conf_fn)


@route('/users/reg',method='POST')
def register_user():
    user_details = request.json
    print user_details, json
    firstname = user_details.get("firstName")
    lastname = user_details.get("lastName")
    email = user_details.get("email")
    password = user_details.get("password")
    db = Storage()
    result = db.insert_registration(firstname, lastname, email, password)
    if result:
        return {"links": [{"url": "/users/login/", "method": "POST"}]}
    else:
        return {"failure": "No body in response."}


@route('/users/login',method='POST')
def login_user():
    email = request.json.get("email")
    password = request.json.get("password")
    db = Storage()
    loginresult = db.checklogin(email, password)
    return {"message": loginresult}


@route('/users/<uid>/boards',method='POST')
def create_board(uid):
    print "uid:" +uid
    print json, request.json
    board_details = request.json
    boardname = board_details.get("boardName")
    print "Board Name: "+boardname
    boardesc = board_details.get("boardDesc")
    print "Board Desc: "+boardesc
    privacy = board_details.get("privacy")
    print "in create board"
    print privacy
    db = Storage()
    result = db.insert_board(boardname, boardesc, privacy, int(uid))
    return {"boardresult": result}

       # return {"failure": "No body in response."}


@route('/users/<uid>/boards/<bname>',method='DELETE')
def delete_board(uid, bname):
    db = Storage()
    deleteStatus = db.deleteBoard(int(uid), bname)
    return {"deleteresult": deleteStatus}


@route('/users/<uid>/boards/<bname>',method='PUT')
def update_board(uid, bname):
   db = Storage()
   boardName = request.json.get("boardName")
   boardDesc = request.json.get("boardDesc")
   privacy = request.json.get("privacy")
   updateStatus = db.updateBoard(int(uid), bname, boardName, boardDesc, privacy)
   return {"updateStatus": updateStatus}


@route('/users/<uid>/boards/<bname>', method='GET')
def getBoardById(uid, bname):
    db = Storage()
    boardStatus = db.getBoardById(int(uid), bname)
    return boardStatus


@route('/users/<uid>/boards', method='GET')
def getUserBoards(uid):
    db = Storage()
    boardsInfo = db.getAllUserBoards(int(uid))
    return boardsInfo

@route('/users/<uid>/allboards', method='GET')
def getAllBoards(uid):
    db = Storage()
    print "in moo"
    allBoards = db.getAllPublicBoards(int(uid))
    return allBoards


@route('/users/<uid>/boards/<boardName>/pins',method="POST")
def create_pin(uid,boardName):
    pinName = request.json.get("pinName")
    description = request.json.get("description")
    db = Storage()
    result = db.insert_pin(pinName,description, boardName, int(uid))
    return result

@route('/users/<uid>/boards/<boardName>/pins/<pinId>',method = 'GET')
def view_pin(uid,boardName,pinId):
    print uid
    print boardName
    print pinId
    db = Storage()
    result = db.getPinById(int(uid),boardName,int(pinId))
    return result

@route('/users/<uid>/boards/<boardName>/pins',method = 'GET')
def list_pins(uid,boardName):
    print uid
    print boardName
    db = Storage()
    result = db.listPins(int(uid),boardName)
    return result

@route('/users/<uid>/boards/<boardName>/pins/<pinId>',method = 'PUT')
def update_pin(uid,boardName,pinId):
    pinN = request.json.get("pinName")
    pinU = request.json.get("description")
    db = Storage()
    result = db.updatePin(int(uid),boardName,pinN,pinU,int(pinId))
    return {"updateStatus": result}

@route('/users/<uid>/boards/<boardName>/pins/<pinId>',method = 'DELETE')
def delete_pin(uid,boardName,pinId):
    db = Storage()
    result = db.deletePin(int(uid),boardName,int(pinId))
    return {"deleteresult": result}

@route('/users/<uid>/boards/<boardName>/pins/<pinId>/comment',method = 'POST')
def insert_comment(uid,boardName,pinId):
    commentD = request.json.get("description")
    db = Storage()
    result = db.insert_comment(commentD,int(pinId),boardName,int(uid))
    return result

@route('/users/<uid>/boards/<boardName>/pins/<pinId>/comment/<cid>', method="GET")
def view_comment(uid,boardName,pinId,cid):
    db = Storage()
    result = db.getCommentById(int(uid),boardName,int(pinId),int(cid))
    return result

@route('/users/<uid>/boards/<boardName>/pins/<pinId>/comments', method="GET")
def view_AllComments(uid,boardName,pinId):
    db = Storage()
    result = db.listComments(int(uid),boardName,pinId)
    return result

@route('/users/<uid>/boards/<boardName>/pins/<pinId>/comment/<cid>', method="DELETE")
def delete_Comment(uid,boardName,pinId,cid):
    db = Storage()
    result = db.deleteComment(int(uid),boardName,int(pinId),int(cid))
    return {"deleteresult": result}

@route('/users/<uid>/boards/<boardName>/pins/<pinId>/comment/<cid>',method='PUT')
def update_comment(uid,boardName,pinId,cid):
    cDesc = request.json.get("description")
    db = Storage()
    result = db.updateComment(int(uid),boardName,cDesc,int(pinId),int(cid))
    return {"updateStatus": result}


#
# setup the configuration for our service
@route('/')
def root():
   print "--> root"
   return 'welcome'

#
#
@route('/moo/ping', method='GET')
def ping():
   return 'ping %s - %s' % (socket.gethostname(),time.ctime())

#
# Development only: echo the configuration of the virtual classroom.
#
# Testing using curl:
# curl -i -H "Accept: application/json" http://localhost:8080/moo/conf
#
# WARN: This method should be disabled or password protected - dev only!
#
@route('/moo/conf', method='GET')
def conf():
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   return room.dump_conf(fmt)

#
# example of a RESTful method. This example is very basic, it does not 
# support much in the way of content negotiation.
#
@route('/moo/echo/:msg')
def echo(msg):
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   if fmt == Room.html:
      return '<h1>%s</h1>' % msg
   elif fmt == Room.json:
      rsp = {}
      rsp["msg"] = msg
      return json.dumps(all)
   else:
      return msg

#
# example of a RESTful query
#
@route('/moo/data/:name', method='GET')
def find(name):
   print '---> moo.find:',name
   return room.find(name)

#
# example adding data using forms
#
@route('/moo/data', method='POST')
def add():
   print '---> moo.add'

   # example list form values
   for k,v in request.forms.allitems():
      print "form:",k,"=",v

   name = request.forms.get('name')
   value = request.forms.get('value')
   return room.add(name,value)

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
   #for key in sorted(request.headers.iterkeys()):
   #   print "%s=%s" % (key, request.headers[key])

   types = request.headers.get("Accept",'')
   subtypes = types.split(",")
   for st in subtypes:
      sst = st.split(';')
      if sst[0] == "text/html":
         return Room.html
      elif sst[0] == "text/plain":
         return Room.text
      elif sst[0] == "application/json":
         return Room.json
      elif sst[0] == "*/*":
         return Room.json

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc

   # default
   return Room.html

#
# The content type on the reply
#
def __response_format(reqfmt):
      if reqfmt == Room.html:
         return "text/html"
      elif reqfmt == Room.text:
         return "text/plain"
      elif reqfmt == Room.json:
         return "application/json"
      else:
         return "*/*"

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc
