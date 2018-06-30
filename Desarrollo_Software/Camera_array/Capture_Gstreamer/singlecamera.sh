#!/bin/bash

export CAPS="video/x-raw(memory:NVMM), width=(int)1640, height=(int)1232, format=(string)I420, framerate=(fraction)30/1"
DISPLAY=:0 gst-launch-1.0 nvcamerasrc sensor-id=0 fpsRange="30 30" ! $CAPS ! autovideosink