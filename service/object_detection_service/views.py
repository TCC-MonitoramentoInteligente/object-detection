import json
import os
import sys

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('{}/../'.format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector
from object_detection_service.models import object_detector_threads, client_ip
from threads.object_detector import ObjectDetector
from threads.video_streaming import VideoStreaming


def messenger(message):
    # TODO: implement async messenger
    print(json.dumps(message))


@csrf_exempt
def register(request):
    if request.method == 'POST':
        detector = Detector()
        detector.load_model()
        port = int(request.POST.get('port'))
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
            return HttpResponse("OK", status=200)
