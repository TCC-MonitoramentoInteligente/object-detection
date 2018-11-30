import paho.mqtt.client as mqtt

from service import settings

cameras_url = 'http://{}:{}/cameras/'\
    .format(settings.USERS_SERVICE_IP, settings.USERS_SERVICE_PORT)

object_detector_threads = {}

mqtt_client = mqtt.Client()
try:
    mqtt_client.connect(settings.BROKER_IP)
except (OSError, ConnectionRefusedError):
    print('Could not connect to broker. Check if it is running and try again.')
    exit(0)

mqtt_client.loop_start()
