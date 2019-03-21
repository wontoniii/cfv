# Instructions for installing YOLO

 https://pjreddie.com/darknet/yolo/

To install YOLO:

``` bash
git clone https://github.com/pjreddie/darknet
cd darknet
make
```

Download pre-trained weights:

```bash
wget https://pjreddie.com/media/files/yolov3.weights
```

# To run the object detector

```bash
cd darknet
./darknet detect cfg/yolov3.cfg yolov3.weights [image path]
```

For example: ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg

To provide image path at runtime, run: ./darknet detect cfg/yolov3.cfg yolov3.weights


