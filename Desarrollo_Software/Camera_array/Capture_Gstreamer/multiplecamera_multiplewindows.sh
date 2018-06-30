#!/bin/bash

export INPUT_CAPS="video/x-raw(memory:NVMM),width=(int)1640,height=(int)1232,format=(string)I420,framerate=(fraction)30/1"
export CONVERT_CAPS="video/x-raw,width=(int)640,height=(int)480,format=(string)I420,framerate=(fraction)30/1"

DISPLAY=:0 gst-launch-1.0 nvcamerasrc sensor-id=0 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink  nvcamerasrc sensor-id=1 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink nvcamerasrc sensor-id=2 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink nvcamerasrc sensor-id=3 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink nvcamerasrc sensor-id=4 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink nvcamerasrc sensor-id=5 fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! xvimagesink -v