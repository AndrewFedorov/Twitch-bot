class Log:
    def addError(self, text):
        Log().writeLog('Error: ' + text)

    def addText(self, text):
        Log().writeLog('Text: ' + text)

    def writeLog(self, text):
        file = open('log.txt', 'a')
        file.write(text + '\n')
        file.close()
        print(text)