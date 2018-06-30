#!/bin/bash

gst-launch-1.0 -v nvcamerasrc sensor-id=1 fpsRange="30 30" num-buffers=100 ! 'video/x-raw(memory:NVMM), width=(int)1640, height=(int)1232, format=(string)I420, \
framerate=(fraction)30/1' ! nvvidconv ! 'video/x-raw, width=(int)1640, height=(int)1232, format=(string)I420, framerate=(fraction)30/1' ! multifilesink location=test_%d.yuv