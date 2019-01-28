import pandas as pd
import paho.mqtt.client as mqtt
import re
import os
import commandcgi
from requests.exceptions import ConnectionError
from time import sleep

cameraid = 1  # トレイルカメラのID
imgPath = "./HORIZON_{0:04d}.JPG".format(cameraid)  # 画像の保存先
host = '127.0.0.1'
port = 1883
topic = 'horizon/img'
keepalive = 60


def toFileList(text):
    fileList = []
    alignText = text.replace(
        "/DCIM/102IMAGE,", "").replace("WLANSD_FILELIST", "").strip()
    for fileElement in alignText.split("\n"):
        fileList.append(fileElement.split(","))
    return fileList


def getFileListText(testMode=False):
    return commandcgi.readTestFileListText() if testMode else commandcgi.readFileListText()


def getLatestFname(df):
    index = -1
    while True:
        if (len(df.index) - index) == -1:
            return ""
        fname = df.iloc[index]["fname"]
        if re.match(r".+\.JPG", fname):
            return fname
        else:
            index = index - 1


def downloadImage(directory, fname, testMode=False):
    os.system(
        "wget http://flashair/DCIM/{0}/{1} -O {2}".format(directory, fname, imgPath))


def toByteArray(path):
    with open(path, "rb") as img:
        return bytes(img.read())


if __name__ == "__main__":
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    while True:
        if commandcgi.isUpdate():
            fileListText = getFileListText()
            if fileListText != "":
                df = pd.DataFrame(toFileList(fileListText), columns=[
                    "fname", "fsize", "attr", "fdate", "ftime"])
                latestFname = getLatestFname(df)
                if latestFname != "":
                    downloadImage("102IMAGE", latestFname)
                    client.connect(host, port=port, keepalive=keepalive)
                    client.publish(topic, toByteArray(imgPath))
                    sleep(0.2)
                    client.disconnect()
                    print("最新の画像ファイルを転送しました")
        sleep(5)  # 秒単位
