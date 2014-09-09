"""
Storage interface
"""

import time
import couchdb.client
from models import User, Board, Pin, Comments


class Storage(object):
    def __init__(self):
        # initialize our storage, data is a placeholder
        self.data = {}
        global couch
        couch = couchdb.Server()  # Assuming localhost:5984
        # couch = couchdb.Server('http://127.0.0.1:5984/')
        global database
        database = couch['pinterest']
        # for demo
        self.data['created'] = time.ctime()
        global user_id
        user_id = 0

    def insert_registration(self, fname, lname, email, password):
        maxval = 0
        for iad in database:
            if (database[iad].get('user_id') > maxval):
                maxval = database[iad].get('user_id')
            print database[iad].get('user_id')

        try:
            user = User(user_id=maxval + 1, FirstName=fname, LastName=lname, email=email, password=password)
            user.store(database)
            print user
            olduser = User.load(database, user.id)
            #print database[iad]
            #database.delete(database[iad])
            return user.id
        except:
            return False

    def checklogin(self, email, password):
        print email
        print password
        for iad in database:
            if (database[iad].get('email') == email) and (database[iad].get('password') == password):
                print database[iad].get('email')
                print database[iad].get('password')

                return "users/" + str(database[iad].get('user_id'))
        return "Login Failed"

    def insert_board(self, bName, bDesc, privacy, userid):
        maxbval = 0
        print "Inside db"
        try:
            print "Inside db try"
            for index in database:
                if (database[index].get('userid') == userid and database[index].get('bid') > maxbval):
                    print database[index].get('bid')
                    maxbval = database[index].get('bid')
            board = Board(boardName=bName, boardDesc=bDesc)
            board['bid'] = maxbval + 1
            board['privacy'] = privacy
            board['userid'] = userid
            board.store(database)
            result = "users/" + str(userid) + "/boards/" + str(board['boardName'])
            print result
            return result
        except:
            print "Exception"

    def getAllUserBoards(self, userid):
        first = 0
        boardsinfo = '{ "boards": [ '
        try:
            for index in database:
                if (database[index].get('userid') == userid):
                    if (first > 0):
                        boardsinfo = boardsinfo + ","
                    boardsinfo = boardsinfo + '{'
                    boardsinfo = boardsinfo + '"BoardId":"' + str(
                        database[index].get('bid')) + '", "BoardName":"' + str(database[index].get('boardName')) + '"}'
                    first = first + 1
            boardsinfo = boardsinfo + ' ] }'
            return boardsinfo
            print boardsinfo
        except:
            print "Get boards Exception"

    def getAllPublicBoards(self, userid):
        print "in storage"
        first = 0
        allBoards = '{ "boards": [ '
        try:
            for index in database:
                if (database[index].get('privacy') == "False" and database[index].get('userid') <> userid):
                    if (first > 0):
                        allBoards = allBoards + ","
                    allBoards = allBoards + '{'
                    allBoards = allBoards + '"BoardId":"' + str(
                        database[index].get('bid')) + '", "BoardName":"' + str(database[index].get('boardName')) + '"}'
                    first = first + 1
            allBoards = allBoards + ' ] }'
            return allBoards
            print allBoards
        except:
            print "Exception in displaying public boards"

    def deleteBoard(self, uid, bname):
        try:
            for index in database:
                if (database[index].get('userid') == uid) and (database[index].get('boardName') == bname):
                    print database[index].get('_id')
                    doc = User.load(database, database[index].get('_id'))
                    database.delete(doc)
                    return "Board deleted"
            return "Board not found"
        except:
            return "Exception in delete"

    def getBoardById(self, uid, bname):
        try:
            for index in database:
                if (database[index].get('userid') == uid) and (database[index].get('boardName') == bname):
                    return '{"BoardId":"' + str(database[index].get('bid')) + '", "BoardName":"' + (
                        database[index].get('boardName')) + '", "BoardDesc":"' + (database[index].get('boardDesc')) + '"}'
            return '{"BoardName":"Board not found"}'
        except:
            return "Exception"

    def updateBoard(self, uid, bname, boardName, boardDesc, privacy):
        #try:
            for index in database:
                if(database[index].get('userid') == uid) and (database[index].get('boardName') == bname):
                    doc = User.load(database, database[index].get('_id'))
                    if boardName is not None:
                        doc['boardName'] = boardName
                    if boardDesc is not None:
                        doc['boardDesc'] = boardDesc
                    if privacy is not None:
                        doc['privacy'] = privacy
                    doc.store(database)
                    return "Document updated"
            return "Board does not exist"
        #except:
            #return "Exception in update"

    def insert_pin(self, pName, pDesc, bName, userid):
        maxpval = 0
        for index in database:
            if(database[index].get('userid')== userid):
                print database[index].get('pin_id')
                maxpval = database[index].get('pin_id')
                print maxpval
                flag = True
                break
            else:
                flag = False

        for index in database:
            if(database[index].get('pin_id')>0):
                maxpval = database[index].get('pin_id')
                print maxpval
            else:
                print "Not Found"


        for iad in database:
            if(database[iad].get('boardName') == bName):
                print iad
                flagcheck = True
                break
            else:
                flagcheck = False

        if(maxpval == None):
            maxpval = 0

        if(flag and flagcheck):
                pin = Pin(pin_name=pName, pin_url=pDesc)
                pin['pin_id'] = maxpval+1
                pin['puserid'] = userid
                pin['board_name'] = bName
                pin.store(database)
                URL = 'url'
                boards = str('/boards/')
                users = str('users/')
                pins = str('/pins/')
                return {"links":[{URL:users+str(userid)+boards+bName+pins+str(pin['pin_id']),"method":"PUT"},{URL:users+str(userid)+boards+bName+pins+str(pin['pin_id']),"method":"GET"},{URL:users+str(userid)+boards+bName+pins+str(pin['pin_id']),"method":"DELETE"}]}
        else:
                return '{"links":[]}'

    def getPinById(self, uid, bName,pID):
        try:
            for index in database:
                print index
                if(database[index].get('pin_id') == pID and database[index].get('puserid') == uid and database[index].get('board_name')==bName):
                    return '{"PinId":"'+ str(database[index].get('pin_id')) +'", "PinName":"'+ (database[index].get('pin_name')) + '", "PinURL":"' + (database[index].get('pin_url')) + '"}'
            return '{"PinName":"Pin Not Found"}'
        except:
            return "Exception in Pin By ID"

    def listPins(self,uid,bName):
        first = 0
        pinInfo = '{ "pins": ['
        try:
            for index in database:
                if(database[index].get('board_name') == bName):
                    if(first>0):
                        pinInfo = pinInfo + ","
                    pinInfo = pinInfo+'{'
                    pinInfo = pinInfo+'"PinId":"' +  str(database[index].get('pin_id')) + '", "PinName":"' + str(database[index].get('pin_name')) + '"}'
                    first = first + 1
            pinInfo = pinInfo+' ] }'
            return  pinInfo
        except:
            print "Get Pins Exception"

    def deletePin(self,uid,bName,pID):
        try:
            for index in database:
                print index
                if(database[index].get('pin_id') == pID and database[index].get('puserid') == uid and database[index].get('board_name')==bName):
                    doc = User.load(database,database[index].get('_id'))
                    database.delete(doc)
            return "Pin Deleted"
        except:
            return "Couldnt be deleted"

    def updatePin(self, uid, bName, pinName, pinURL,pinID):
       try:
           for index in database:
               if(database[index].get('pin_id') == pinID and database[index].get('puserid') == uid and database[index].get('board_name')==bName):
                   doc = User.load(database, database[index].get('_id'))
                   if pinName is not None:
                        doc['pin_name'] = pinName
                   if pinURL is not None:
                        doc['pin_url'] = pinURL
                   doc.store(database)
                   return "Document updated"
           return "Pin does not exist"
       except:
           return "Exception in update PIN"

    def insert_comment(self,commentDesc,pID,bName,userid):
        maxcval = 0
        for index in database:
            if(database[index].get('userid')== userid):
                flag = True
                break
            else:
                flag = False

        for index in database:
            if(database[index].get('pin_id')== pID):
                print database[index].get('pin_id')
                flagpin = True
                break
            else:
                flagpin = False

        for index in database:
            if(database[index].get('commentid')>0):
                maxcval = database[index].get('commentid')
                print maxcval
            else:
                print "Not Found"

        for iad in database:
            if(database[iad].get('boardName') == bName):
                print iad
                flagcheck = True
                break
            else:
                flagcheck = False

        if(maxcval == None):
            maxcval = 0

        if(flag and flagcheck and flagpin):
                comment = Comments(commentDesc=commentDesc)
                comment['commentid'] = maxcval+1
                comment['cuserid'] = userid
                comment['cboard_name'] = bName
                comment['cpin_id'] = pID
                comment.store(database)
                URL = 'url'
                boards = str('/boards/')
                users = str('users/')
                pins = str('/pins/')
                comments = str('/comment/')
                return {"links":[{URL:users+str(userid)+boards+bName+pins+str(pID)+comments+str(comment['commentid']),"method":"PUT"},{URL:users+str(userid)+boards+bName+pins+str(pID)+comments+str(comment['commentid']),"method":"GET"},{URL:users+str(userid)+boards+bName+pins+str(pID)+comments+str(comment['commentid']),"method":"DELETE"}]}
        else:
                return '{"links":[]}'

    def getCommentById(self,uid,bName,pID,commentId):
        try:
            for index in database:
                if(database[index].get('cpin_id') == pID and database[index].get('cuserid') == uid and database[index].get('cboard_name')==bName and database[index].get('commentid') == commentId):
                    return '{"CommentId":"'+ str(database[index].get('commentid')) +'", "Description":"'+ (database[index].get('commentDesc')) + '" }'
            return '{"Description":"Comment Not Found"}'
        except:
            return "Exception in Comment By ID"

    def listComments(self,uid,bName,pID):
        first =0
        commentsInfo = '{ "Comments": ['
        try:
            for index in database:
                if(database[index].get('cboard_name') == bName):
                    if(first>0):
                        commentsInfo = commentsInfo + ","
                    commentsInfo = commentsInfo+'{'
                    commentsInfo = commentsInfo+'"CommentsId":"' +  str(database[index].get('commentid')) + '", "CommentDescription":"' + str(database[index].get('commentDesc')) + '"}'
                    first = first + 1
            commentsInfo = commentsInfo+' ] }'
            return  commentsInfo
        except:
            print "Get Comments Exception"


    def deleteComment(self,uid,bName,pID,commentID):
        try:
            for index in database:
                print index
                if(database[index].get('cpin_id') == pID and database[index].get('cuserid') == uid and database[index].get('cboard_name')==bName and database[index].get('commentid') == commentID):
                    doc = User.load(database,database[index].get('_id'))
                    database.delete(doc)
            return "Comment Deleted"
        except:
            return "Couldnt be deleted"

    def updateComment(self, uid, bName,commentDesc,pinID,commentID):
       try:
           for index in database:
               if(database[index].get('cpin_id') == pinID and database[index].get('cuserid') == uid and database[index].get('cboard_name')==bName and database[index].get('commentid')==commentID):
                   doc = User.load(database, database[index].get('_id'))
                   if commentDesc is not None:
                        doc['commentDesc'] = commentDesc
                   doc.store(database)
                   return "Document updated"
           return "Comment does not exist"
       except:
           return "Exception in update Comment"

    def remove(self, name):
        print "---> remove:", name

    def names(self):
        print "---> names:"
        for k in self.data.iterkeys():
            print 'key:', k

    def find(self, name):
        print "---> storage.find:", name
        if name in self.data:
            rtn = self.data[name]
            print "---> storage.find: got value", rtn
            return rtn
        else:
            return None
