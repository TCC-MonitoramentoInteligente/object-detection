# Object detection service

The object detector is [A PyTorch implementation of a YOLO v3 Object Detector](https://github.com/ayooshkathuria/pytorch-yolo-v3). This service receives real time video, detects objects and sends the detections back asynchronously to a message broker.

# Requirements
- Ubuntu 16.04 with good GPU
- ZeroTier
- OpenCV
- Nvidia CUDA
- Python 3

## Setup
From `object-detection/`, do:
1. Install OpenCV library `$ sudo apt-get install libopencv-dev python-opencv`
2. Install Nvidia CUDA-9.0, following this [tutorial](https://yangcha.github.io/CUDA90/) or running the `cuda.sh` script for Ubuntu 16.04
3. Create virtualenv `$ virtualenv --system-site-packages -p python3 venv`
4. Activate virtualenv `$ source venv/bin/activate`
5. Install requirements `$ pip install -r requirements.txt`
6. Download YOLO pre-trained weight file `$ wget https://pjreddie.com/media/files/yolov3.weights -P weights/`
7. Install [ZeroTier](https://www.zerotier.com/download.shtml) and create a new network
8. Set the variables `GPU_SERVER_IP` and `BROKER_IP` (`object-detection/service/service/settings.py`) with respectives ZeroTier IPs.

## Testing
### Testing the module
There is a simple script to test if the detector module is working, to verify that the environment has been correctly configured. Run `$ python3 test/detector_test.py --image /path/to/image`. You should see a list with all the detected objects.

## API
- `http://<GPU_SERVER_IP>:8000/object-detection/register/`: to use the service, you need to request a new thread to process your video streaming. The response is a free port number where you should transmit the video streaming `(GPU_SERVER_IP, port)`
  - Method: POST
  - Data:
    - `cam_id`: Camera ID
  - Request response: a free port number where you should transmit your video
  - Detection asynchronous and continuous response: The response is a JSON object, sent asynchronously to the message broker, with ZeroTier IP `BROKER_IP`
    - `cam_id`: Camera ID
    - `time`: frame time, in seconds
    - `objects`: a list of dicts, containing the detected objects

- `http://<GPU_SERVER_IP>:8000/object-detection/monitor/`: If you need to see the output of the detections, pass the address you want the service to transmit. You can visualise the video with [python-live-video-streaming](https://github.com/jhonata-antunes/python-live-video-streaming) server
  - Method: POST
  - Data:
    - `client_ip`: IP address to transmit the video with detections
    - `client_port`: port

- `http://<GPU_SERVER_IP>:8000/object-detection/unregister/`: if object detection is no longer necessary or you want to register again to get a new port
  - Method: POST
  - Data:
    - `cam_id`: Camera ID

- `http://<GPU_SERVER_IP>:8000/object-detection/event_print/`: return a print of the video streaming
  - Method: GET
  - Parameters:
    - `cam_id`: Camera ID
  - Response: a base64 encoded image print of the video streaming

- `http://<GPU_SERVER_IP>:8000/object-detection/status/`: processing status
  - Method: GET
  - Response: a list with the status of all videos streaming being processed

## Run
`$ python3 service/manage.py runserver <GPU_SERVER_IP>:8000`

## Usage
1. Register and receive a free port
2. Start your video submission, running [python-live-video-streaming](https://github.com/jhonata-antunes/python-live-video-streaming) client `$ python3 client.py --ip <GPU_SERVER_IP> --port <new port>` or `$ python3 client.py --ip <GPU_SERVER_IP> --port <new port> --video /path/to/video.mp4`
3. On the same machine or on a different machine, you must have a message broker installed and running. Register to the `object-detection/objects` topic to receive the detected objects