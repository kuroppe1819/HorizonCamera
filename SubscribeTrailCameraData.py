import paho.mqtt.client as mqtt

cameraid = 1  # トレイルカメラのID
imgPath = "./SUB_HORIZON_{0:04d}.JPG".format(cameraid)  # 画像の保存先
host = '127.0.0.1'
port = 1883
topic = 'horizon/img'
keepalive = 60


def onConnect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(topic)


def onMessage(client, userdata, msg):
    with open(imgPath, 'wb') as f:
        f.write(msg.payload)
    print("画像ファイルを受信しました")


def onSubscribe():
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.on_connect = onConnect
    client.on_message = onMessage
    client.connect(host, port=port, keepalive=keepalive)
    client.loop_forever()


if __name__ == "__main__":
    onSubscribe()
