# Object detecton module

[NOTE]: Future updates will change this module to a independent service. Now, it is a Python interface, and after, will become a REST API.

The detector is [A PyTorch implementation of a YOLO v3 Object Detector](https://github.com/ayooshkathuria/pytorch-yolo-v3). This module is a Python interface to the YOLO model.

## Setup
1. Install Nvidia CUDA-9.0, following this [tutorial](https://yangcha.github.io/CUDA90/);
2. Create virtualenv `$ virtualenv --system-site-packages -p python3 venv`;
3. Activate virtualenv `$ source venv/bin/activate`;
4. Install requirements `$ pip install -r requirements.txt`;
5. Download YOLO pre-trained weight file `$ wget https://pjreddie.com/media/files/yolov3.weights`.

## Usage
```
from detector import Detector

detector = Detector()
detector.load_model()

...

object_list = detector.detect(frame)
```
The `Detector.detetc` function returns a list of `Object` containing all objects detected by the model
```
class Object:
    """
    Represents a detected object
    """
    # (x, y) is the top left coordinate
    x = None
    y = None
    width = 0
    height = 0
    label = None
    score = .0
```
