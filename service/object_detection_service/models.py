import paho.mqtt.client as mqtt

from service import settings

cameras_url = 'http://{}:{}/cameras/'\
    .format(settings.USERS_SERVICE_IP, settings.USERS_SERVICE_PORT)

object_detector_threads = {}

mqtt_client = mqtt.Client()
mqtt_client.connect(settings.BROKER_IP)
mqtt_client.loop_start()
