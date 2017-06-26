import config
from urllib.request import urlopen, Request
import json
import time
from time import sleep
import datetime
import _mysql


def mess(sock, message):
    sock.sendall("PRIVMSG #{} :{}\r\n".format(config.CHAN, message).encode("utf-8"))

def ban(sock, user):
    mess(sock, ".ban {}".format(user))

def timeout(sock, user, seconds = 500):
    mess(sock, ".timeout {}".format(user, seconds))

def fillOpList():

    db = _mysql.connect(host="localhost", user="root", passwd="qwerty123456", db="mydb")
    current_time = datetime.datetime.now()
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/djarii/chatters"
            req = Request(url, headers={"accept": "*/*"})
            res = urlopen(req).read()
            config.oplist.clear()
            data = json.loads(res)
            
            db_viewers = []
            db.query("SELECT NickName, Points FROM viewers")
            sql_res = db.store_result().fetch_row()
            print(sql_res)
            if len(sql_res) > 0:
                db_viewers = sql_res[0]
            
            for viewer in config.viewers:
                for db_viewer in db_viewers:
                    if viewer not in db_viewer[0]:
                        
            
            for type in data["chatters"]:
                for viewer in data["chatters"][type]:
                    if viewer not in config.viewers:
                        
                        if len(result) > 0:
                            config.viewers[viewer] = int(result[0][0])
                        else:
                            config.viewers[viewer] = config.START_POINTS
                        print(str(config.viewers[viewer]) + ' ' + viewer)
                        
        except Exception as e:
            print(str(e))

        points = round((datetime.datetime.now() - current_time).total_seconds()/60)
        for viewer in config.viewers:
            config.viewers[viewer] += points
            db.query("SELECT EXISTS (SELECT 1 FROM viewers WHERE NickName = '{0}' LIMIT 1)".format(viewer))
            result = bool(int(db.store_result().fetch_row()[0][0]))
            if result:
                db.query("UPDATE viewers SET Points = {1} WHERE NickName = '{0}'".format(viewer, config.viewers[viewer]))
            else:
                db.query("INSERT INTO viewers (NickName, Points) VALUES ('{0}', {1})".format(viewer, config.viewers[viewer]))
        
        sleep(5)



def isOp(user):
    return user in config.oplist