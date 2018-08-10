import json
import os
import sys

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('{}/../'.format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector
from object_detection_service.models import client_ip, mqtt_client, object_detector_threads
from threads.object_detector import ObjectDetector
from threads.video_streaming import VideoStreaming


def messenger(message):
    mqtt_client.publish(topic="object-detection/objects", payload=json.dumps(message))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        port = request.POST.get('port')
        try:
            int(port)
        except ValueError:
            return HttpResponse("Value {} can't be converted to integer".format(port),
                                status=400)
        for od in object_detector_threads:
            if od.get_id() is None:
                object_detector_threads.remove(od)
            elif od.get_id() == port:
                return HttpResponse("Port {} is already in use".format(port), status=400)
        detector = Detector()
        detector.load_model()
        vs = VideoStreaming(ip=client_ip, port=port)
        od = ObjectDetector(vs=vs, detector=detector, messenger=messenger)
        od.start()
        object_detector_threads.append(od)
        return HttpResponse("OK", status=200)


@csrf_exempt
def unsubscribe(request):
    if request.method == 'POST':
        od_id = request.POST.get('port')
        object_detector = None
        for od in object_detector_threads:
            if od.get_id() == od_id:
                object_detector = od
                break
        if object_detector is None:
            return HttpResponse("Port {} not found".format(od_id), status=404)
        else:
            object_detector.kill()
            object_detector_threads.remove(object_detector)
            return HttpResponse("OK", status=200)
