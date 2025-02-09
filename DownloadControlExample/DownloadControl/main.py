import paho.mqtt.client as mqtt
import logging
from time import sleep

BROKER = "localhost"
PORT = 1883
TOPIC_SUBSCRIBE = "mender/update/enter"
TOPIC_PUBLISH = "mender/update/response"

USER_PREFERENCE = "21"  # Retry Later
# USER_PREFERENCE = "0"  # Proceed
# USER_PREFERENCE = "1"  # Skip Update

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)


def on_connect(mqttclient, userdata, flags, rc):
    if rc == 0:
        logging.info(f"Connected to MQTT broker at {BROKER}:{PORT}")
        mqttclient.subscribe(TOPIC_SUBSCRIBE)
    else:
        logging.info(f"Failed to connect, return code {rc}")


def on_message(mqttclient, userdata, msg):
    _status = msg.payload.decode("utf-8")
    logging.info(f"[DownloadControl] Received Status -> {_status}")
    sleep(1)
    if _status == "download":
        logging.info(f"[DownloadControl] Publishing -> {USER_PREFERENCE}")
        mqttclient.publish(TOPIC_PUBLISH, str(USER_PREFERENCE))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker and start the loop
client.connect(BROKER, PORT, 60)
client.loop_forever()
