import base64
from io import BytesIO

import cv2
import json
import os
import sys

from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service import settings

sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('{}/../'.format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector
from object_detection_service.models import mqtt_client, object_detector_threads
from threads.object_detector import ObjectDetector
from threads.video_streaming import VideoStreaming


def messenger(message):
    mqtt_client.publish(topic="object-detection/objects", payload=json.dumps(message))


def on_detection_finish(od_id):
    del object_detector_threads[od_id]
    mqtt_client.publish(topic="object-detection/remove", payload=od_id)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        cam_id = request.POST.get('cam_id')
        debug_ip = request.POST.get('debug_ip')
        if object_detector_threads.get(cam_id) is not None:
            return HttpResponse("Camera {} is already registered".format(cam_id), status=400)
        detector = Detector()
        detector.load_model()
        vs = VideoStreaming(settings.GPU_SERVER_IP, cam_id)
        od = ObjectDetector(vs, detector, messenger, on_detection_finish, debug_ip)
        od.start()
        object_detector_threads[cam_id] = od
        mqtt_client.publish(topic="object-detection/add", payload=cam_id)
        return HttpResponse(od.get_port(), status=200)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def unsubscribe(request):
    if request.method == 'POST':
        cam_id = request.POST.get('cam_id')
        object_detector = object_detector_threads.get(cam_id)
        if object_detector is None:
            return HttpResponse("Camera {} not found".format(cam_id), status=404)
        else:
            object_detector.kill()
            return HttpResponse("OK", status=200)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def status(request):
    if request.method == 'GET':
        response = []
        for cam_id, od in object_detector_threads.items():
            response.append({
                'id': od.get_id(),
                'video_fps': od.get_video_fps(),
                'detection_fps': od.get_detection_fps(),
            })
        return JsonResponse(response, safe=False)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def event_print(request):
    if request.method == 'GET':
        cam_id = request.GET.get('cam_id')
        object_detector = object_detector_threads.get(cam_id)
        if object_detector is None:
            return HttpResponse("Camera {} not found".format(cam_id), status=404)
        frame = object_detector.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(frame)
        buffered = BytesIO()
        pil_frame.save(buffered, format="JPEG")
        b64 = base64.b64encode(buffered.getvalue())
        return HttpResponse(b64, status=200)
    else:
        return HttpResponse("Method not allowed", status=405)
