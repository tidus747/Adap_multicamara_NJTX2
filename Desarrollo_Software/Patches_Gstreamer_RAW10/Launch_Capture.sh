
#!/bin/bash

# Script para lanzar capturas de imagen usando Gstreamer
# Master en Ingenieria Industrial
# Ivan Rodriguez Mendez

export VERSION=1.8.0
export LD_LIBRARY_PATH=/home/$USER/gst_$VERSION/out/lib/


gst-launch-1.0 -vvv v4l2src num-buffers=10  ! 'video/x-bayer, width=(int)1920, height=(int)1080, format=(string)rggb, framerate=(fraction)30/1' ! multifilesink location=test%d.raw  -v
