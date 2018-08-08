import paho.mqtt.client as mqtt


client_ip = "localhost"
object_detector_threads = []

mqtt_client = mqtt.Client()
mqtt_client.connect(client_ip)
