# Object detection service

The detector is [A PyTorch implementation of a YOLO v3 Object Detector](https://github.com/ayooshkathuria/pytorch-yolo-v3). This service receives real time video, detects objects and prints the results.

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

## Usage
 - First, clone [python-live-video-streaming](https://github.com/jhonata-antunes/python-live-video-streaming) repo. It contains the video streaming server.
 - Run the service `$ python3 service/manage.py runserver`.
 - Inscrible a new video transmission `$ curl --data "port=5005". http://127.0.0.1:8000/object-detection/register/`, passing the port where the video is being transmitted to.
 - Start video streaming `$ python3 server.py --video /path/to/video/file --port 5005`.
 - If you don not want to process video any more, unsubscribe `$ curl --data "port=5005" http://127.0.0.1:8000/object-detection/unsubscribe/`.