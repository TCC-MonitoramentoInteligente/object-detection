import ast

import numpy as np

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import detector


@csrf_exempt
def detect(request):
    if request.method == 'POST':
        # if detector.is_ready():
        #     data = request.data
        #     print(data)
        #     return HttpResponse(status=200)
        # else:
        #     return HttpResponse("Detector module is not ready", status=500)
        # img = np.fromstring(request.POST['image'], dtype=np.float32)

        shape = ast.literal_eval(request.POST.get('shape'))
        img_bytes = request.POST.get('image')
        print(img_bytes)
        print(len(img_bytes))
        # Here we reconstruct the image
        # img = np.fromstring(img_bytes, dtype=np.uint8).reshape(shape)
        return JsonResponse({'image': 'Hello', 'shape': shape})
