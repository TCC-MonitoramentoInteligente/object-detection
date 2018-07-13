import ast
import base64
import json

import numpy as np

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import detector


@csrf_exempt
def detect(request):
    if request.method == 'POST':
        if detector.is_ready():
            shape = ast.literal_eval(request.POST.get('shape'))
            buffer = base64.b64decode(request.POST.get('frame'))
            # Reconstruct the image
            frame = np.frombuffer(buffer, dtype=np.uint8).reshape(shape)
            object_list = detector.detect(frame)
            json_string = json.dumps([obj.__dict__() for obj in object_list])
            return JsonResponse({'object_list': json_string})
        else:
            return HttpResponse("Detector module is not ready", status=500)
