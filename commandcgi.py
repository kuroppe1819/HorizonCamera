import requests


def getResponseCommandCgiText(parameter, directory=""):
    url = "http://flashair/command.cgi?"
    try:
        response = requests.get("{0}{1}{2}".format(url, parameter, directory))
        response.encoding = response.apparent_encoding
        return response.text
    except ConnectionError:
        print("FlashAirとの接続に失敗しました: parameter->{0}".format(parameter))
        return ""


def readTestFileListText():
    with open("getfilename") as f:
        return f.read()


def readFileListText(): return getResponseCommandCgiText(
    parameter="op=100&DIR=/DCIM/", directory="102IMAGE")


def isUpdate(testMode=False):
    return True if testMode or int(getResponseCommandCgiText(parameter="op=102")) == 1 else False
