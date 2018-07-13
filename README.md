# Object detection service

The detector is [A PyTorch implementation of a YOLO v3 Object Detector](https://github.com/ayooshkathuria/pytorch-yolo-v3). This service is a REST API interface to the YOLO model.

## Setup
From `object-detection/`, do:
1. Install Nvidia CUDA-9.0, following this [tutorial](https://yangcha.github.io/CUDA90/);
2. Create virtualenv `$ virtualenv --system-site-packages -p python3 venv`;
3. Activate virtualenv `$ source venv/bin/activate`;
4. Install requirements `$ pip install -r requirements.txt`;
5. Download YOLO pre-trained weight file `$ wget https://pjreddie.com/media/files/yolov3.weights -P weights/`.

## Testing
### Testing the module
There is a simple script to test if the detector module is working, to verify that the environment has been correctly configured. Run `$ python3 detector_test.py --image /path/to/image`. You should see a list with all the detected objects, represented by the model/Object class.
### Testing the API
There is a script to test the service, using image or video. The first thing to do is run the server `$ python3 service/manage.py runserver --noreload`. The second, open a new tab and run the script to test either with image `$ python3 service_test.py --image /path/to/image` or video `$ python3 service_test.py --video /path/to/video`. To close OpenCV's window, press `q`.

## Usage
Make a POST to `http://localhost:8000/detect/`, with the following object:
```
{
    'frame': frame # numpy array encoded in base64 
    'shape': shape # tuple (width, height, channels)
}
```
The response is a list containing all detected objects:
```
[
    {
        # (x, y) is the top left coordinate
        'x': 0,
        'y': 0,
        # (x2, y2) is the bottom right coordinate
        'x2': 0,
        'y2': 0,
        'width': 0,
        'height': 0,
        'label': "",
        'score': 0.0,
    },
]
```
