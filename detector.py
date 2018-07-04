import torch


class Detector:
    _model = None
    _dataset = "pascal"
    _confidence = 0.5
    _nms_thresh = 0.4
    _cfg = "cfg/yolov3.cfg"
    _weights = "weights/yolov3.weights"
    _resolution = "416"
    _cuda = False
    _num_classes = 80
    _classes = None

    def __del__(self):
        torch.cuda.empty_cache()

    def set_dataset(self, dataset: str):
        """
        :param dataset: Dataset on which the network has been trained
        :return:
        """
        if type(dataset) is not str:
            raise TypeError("dataset must be a string!")
        self._dataset = dataset

    def set_confidence(self, confidence: float):
        """
        :param confidence: Object Confidence to filter predictions
        :return:
        """
        if type(confidence) is not float:
            raise TypeError("confidence must be a float!")
        self._confidence = confidence

    def set_nms_thresh(self, nms_thresh: float):
        """
        :param nms_thresh: NMS Threshold
        :return:
        """
        if type(nms_thresh) is not float:
            raise TypeError("mns_thresh must be a float!")
        self._nms_thresh = nms_thresh

    def set_cfg(self, cfg: str):
        """
        :param cfg: Path to config file
        :return:
        """
        if type(cfg) is not str:
            raise TypeError("cfg must be a string!")
        self._cfg = cfg

    def set_weights(self, weights: str):
        """
        :param weights: Path to weights file
        :return:
        """
        if type(weights) is not str:
            raise TypeError("weights must be a string!")
        self._weights = weights

    def set_resolution(self, resolution: str):
        """
        :param resolution: Input resolution of the network.
        Increase to increase accuracy. Decrease to increase speed.
        :return:
        """
        if type(resolution) is not str:
            raise TypeError("resolution must be a string!")
        self._resolution = resolution
