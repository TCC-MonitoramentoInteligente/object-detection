import base64
from io import BytesIO

import cv2
import os
import sys
import json

import requests
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service import settings

sys.path.append('{}/../../'.format(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('{}/../'.format(os.path.dirname(os.path.abspath(__file__))))

from detector import Detector
from object_detection_service.models import cameras_url, mqtt_client, object_detector_threads
from threads.object_detector import ObjectDetector
from threads.video_streaming import VideoStreaming


def messenger(message):
    mqtt_client.publish(topic="object-detection/objects", payload=json.dumps(message))


def on_detection_finish(cam_id, timeout):
    del object_detector_threads[cam_id]
    mqtt_client.publish(topic="object-detection/remove", payload=cam_id)
    if timeout:
        mqtt_client.publish(topic="object-detection/logs/success",
                            payload='Camera {} was unregistered automatically by timeout'.format(cam_id))


@csrf_exempt
def register(request):
    already_registered = 'Register error. Camera {} is already registered.'
    not_allowed = 'Register error. Camera {} not allowed.'
    user_not_responding = 'Register error. Users service is not responding. ' \
                          'Unable to check camera permission.'
    success = 'Camera {} was successfully registered'

    if request.method == 'POST':
        cam_id = request.POST.get('cam_id')
        if object_detector_threads.get(cam_id) is not None:
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=already_registered.format(cam_id))
            return HttpResponse(already_registered.format(cam_id), status=400)

        try:
            url = cameras_url + '{}/'.format(cam_id)
            cam_request = requests.get(url, timeout=4)
            response_id = cam_request.json()['id']
            if cam_request.status_code != requests.codes.ok or response_id != cam_id:
                mqtt_client.publish(topic="object-detection/logs/error",
                                    payload=not_allowed.format(cam_id))
                return HttpResponse(not_allowed.format(cam_id), status=403)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=user_not_responding.format(cam_id))
            return HttpResponse(user_not_responding.format(cam_id), status=500)

        detector = Detector()
        detector.load_model()
        vs = VideoStreaming(settings.GPU_SERVER_IP, cam_id)
        od = ObjectDetector(vs, detector, messenger, on_detection_finish)
        od.start()
        object_detector_threads[cam_id] = od
        mqtt_client.publish(topic="object-detection/add", payload=cam_id)
        mqtt_client.publish(topic="object-detection/logs/success",
                            payload=success.format(cam_id))
        return HttpResponse(od.get_port(), status=200)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def monitor(request):
    not_found = 'Monitor error. Camera {} not found.'
    bad_request = 'Monitor error. Invalid address ({}, {}). Port must be an integer.'
    success = 'Monitor success. Sending video to address ({}, {}).'

    if request.method == 'POST':
        cam_id = request.POST.get('cam_id')
        client_ip = request.POST.get('client_ip')
        client_port = request.POST.get('client_port')
        object_detector = object_detector_threads.get(cam_id)
        if object_detector is None:
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=not_found.format(cam_id))
            return HttpResponse(not_found.format(cam_id), status=404)
        try:
            client_port = int(client_port)
        except TypeError:
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=bad_request.format(client_ip, client_port))
            return HttpResponse(bad_request.format(client_ip, client_port), status=400)
        object_detector.monitor(client_ip, client_port)
        mqtt_client.publish(topic="object-detection/logs/success",
                            payload=success.format(client_ip, client_port))
        return HttpResponse(success.format(client_ip, client_port), status=200)
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
def unregister(request):
    not_found = 'Unregister error. Camera {} not found.'
    success = 'Camera {} was successfully unregistered'

    if request.method == 'POST':
        cam_id = request.POST.get('cam_id')
        object_detector = object_detector_threads.get(cam_id)
        if object_detector is None:
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=not_found.format(cam_id))
            return HttpResponse(not_found.format(cam_id), status=404)
        object_detector.kill()
        mqtt_client.publish(topic="object-detection/logs/success",
                            payload=success.format(cam_id))
        return HttpResponse(success, status=200)
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
    not_found = 'Event print error. Camera {} not found.'
    success = 'An event print was requested from camera {}'

    if request.method == 'GET':
        cam_id = request.GET.get('cam_id')
        object_detector = object_detector_threads.get(cam_id)
        if object_detector is None:
            mqtt_client.publish(topic="object-detection/logs/error",
                                payload=not_found.format(cam_id))
            return HttpResponse(not_found.format(cam_id), status=404)
        frame = object_detector.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(frame)
        buffered = BytesIO()
        pil_frame.save(buffered, format="JPEG")
        b64 = base64.b64encode(buffered.getvalue())
        mqtt_client.publish(topic="object-detection/logs/success",
                            payload=success.format(cam_id))
        return HttpResponse(b64, status=200)
    else:
        return HttpResponse("Method not allowed", status=405)
