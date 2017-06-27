import sys, os 
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import cgi
import help_func
from log import Log

form = cgi.FieldStorage()
create = form.getfirst("create", None)
close = form.getfirst("close", None)
finish = form.getfirst("finish", None)
Log().addText(str(form))

if close:
    help_func.Bet.close()
elif finish:
    winword = form.getfirst("winword", None)
    if winword:
        help_func.Bet.finish(winword)
elif create:
    question = form.getfirst("question", None)
    keywords = []
    keyword = None
    while True:
        keyword = form.getfirst("keyword" + str(len(keywords)), None)
        if not keyword:
            break
        keywords.append(keyword)

    if len(keywords) > 0:
        help_func.Bet.create(question, keywords)

print('Status: 302 Found')
print("Content-type: text/html\n")
print('<html><head><meta http-equiv="refresh" content="0;url=http://localhost:8000" /></head></html>')