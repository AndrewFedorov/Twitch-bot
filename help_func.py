from config import viewers, CHAN, DB_HOST, DB_USER, DB_PASS, DB_SCHEME, START_POINTS, type_viewer
from urllib.request import urlopen, Request
import time
import json
import _mysql
from log import Log


class TimeKeeper:
    last_send = 0

def sendToTwitch(sock, message):
    if int(time.time()) - TimeKeeper.last_send > 2: # that's condition Twitch, no more than 20 messages within 30 sec
        try:
            sock.sendall("PRIVMSG #{} :{}\r\n".format(CHAN, message).encode("utf-8"))
            TimeKeeper.last_send = int(time.time())
            Log().addText('sended to Twitch: {0}'.format(message))
        except Exception as e:
            Log().addError('Error while send to Twitch: {0}; Error text: {1}'.format(message, str(e)))

class DB:
    db_connect = None

    def __init__(self):
        if not DB.db_connect:
            Log().addText('DB init')
            DB.db_connect = _mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_SCHEME)

    def updateViewer(self, viewer, points):
        db = DB.db_connect
        db.query("SELECT EXISTS (SELECT 1 FROM viewers WHERE NickName = '{0}' LIMIT 1)".format(viewer))
        result = bool(int(db.store_result().fetch_row()[0][0]))
        if result:
            db.query("UPDATE viewers SET Points = Points + {1} WHERE NickName = '{0}'".format(viewer, points))
        else:
            db.query("INSERT INTO viewers (NickName, Points, Type) VALUES ('{0}', {1}, {2})".format(viewer, START_POINTS + points, viewers[viewer] + 1))

    def createTables(self):
        db = DB.db_connect
        db.query('''
            CREATE TABLE IF NOT EXISTS `Viewers` (
            `@Viewers` INT NOT NULL AUTO_INCREMENT,
            `NickName` TEXT NOT NULL,
            `Points` INT NULL,
            `Type` ENUM('moderators', 'staff', 'admins', 'global_mods', 'viewers') NULL,
            PRIMARY KEY (`@Viewers`))
            ENGINE = InnoDB
        ''')

    def getPoints(self, nickname):
        db = DB.db_connect
        db.query("SELECT Points FROM viewers WHERE NickName = '{0}' LIMIT 1".format(nickname))
        res_sql = db.store_result().fetch_row()
        if len(res_sql) > 0 and len(res_sql[0]) > 0:
            return res_sql[0][0]

def fillListOfViewers():
    while True:
        try:
            # get list of viewers
            url = 'http://tmi.twitch.tv/group/user/{0}/chatters'.format(CHAN)
            req = Request(url, headers={"accept": "*/*"})
            res = urlopen(req).read()
            data = json.loads(res)   
            # fill list of viewers
            viewers.clear()
            for type in data["chatters"]:
                for viewer in data["chatters"][type]:
                    enum_type = None
                    if type in type_viewer:
                        enum_type = type_viewer.index(type)
                    viewers[viewer] = enum_type
            
            # save viewers in DB
            for viewer in viewers:
                DB().updateViewer(viewer, 1)
        
        except Exception as e:
            Log().addError('Error while fill list of viewers: {0}'.format(str(e)))
        
        time.sleep(60)

class BetKeeper:
    status = False
    keywords = []
    bets = {}

class Bet:
    status = False
    keywords = []
    bets = {}

    @staticmethod
    def create(question, kwords):
        for keyword in kwords:
            BetKeeper.keywords.append(keyword.lower())
        BetKeeper.status = True
        Log().addText('Bet created: Question: {0}, Keywords: {1}'.format(question, BetKeeper.keywords))

    @staticmethod
    def make(nickname, message):
        print(BetKeeper.status)
        if BetKeeper.status and len(BetKeeper.keywords) > 0:
            print('2')
            bet_info = message.split(' ')
            if bet_info > 3:
                print('3')
                keyword = bet_info[1].lower()
                size_bet = bet_info[2]
                if keyword in BetKeeper.keywords and size_bet.isdigit():
                    BetKeeper.bets[nickname] = (keyword, size_bet)
                    Log().addText('Bet: nickname: {0}, keyword:{1}, size_bet:{2}'.format(nickname, keyword, size_bet))

    @staticmethod
    def close():
        BetKeeper.status = False
        Log().addText('Bet closed')

    @staticmethod
    def finish(winword):
        for nickname in BetKeeper.bets:
            points = BetKeeper.bets[nickname][1]
            is_win = 1 if BetKeeper.bets[nickname][0] == winword.lower() else -1
            DB().updateViewer(viewer, is_win*points)
        Log().addText('Bet finished: winword: {0}'.format(winword))