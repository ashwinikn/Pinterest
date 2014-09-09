__author__ = 'neema'

from couchdb.mapping import Document, TextField, IntegerField, ListField, DictField, Mapping


class User(Document):
    user_id = IntegerField()
    FirstName = TextField()
    LastName = TextField()
    email = TextField()
    password = TextField()


class Pin(Document):
    pin_id = IntegerField()
    pin_url = TextField()
    pin_name = TextField()
    board_name = TextField()
    #comments = ListField(DictField(Mapping.build(_id=IntegerField(),
                                                # comment=TextField())))


class Board(Document):
    bid = IntegerField()
    boardName = TextField()
    boardDesc = TextField()
    isPrivate = bool()
    #pins = ListField(DictField(Mapping.build(pin_id=IntegerField())))


class Comments(Document):
    commentid = IntegerField()
    commentDesc = TextField()
    cpin_id = IntegerField()
    cboard_name = TextField()