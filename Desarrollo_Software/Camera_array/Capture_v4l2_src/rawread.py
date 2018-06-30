'''
This file is part of the University of la Laguna distribution.
Copyright (c) 2018 Ivan Rodriguez Mendez and Fernado Luis Rosa Gonzalez.
 
This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import numpy as np
import struct as st
import cv2

def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()

def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix

def simplest_cb(img, percent):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    channels = cv2.split(img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        # find the low and high precentile values (based on the input percentile)
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]
        f = int(np.floor(n_cols * half_percent))
        low_val  = flat[f]
        high_val = flat[int(np.ceil( n_cols * (1.0 - half_percent)))]

        print "Lowval: ", low_val
        print "Highval: ", high_val

        # saturate below the low percentile and above the high percentile
        thresholded = apply_threshold(channel, low_val, high_val)
        # scale the channel
        normalized = cv2.normalize(thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    return cv2.merge(out_channels)

def apply_percentil(filename, modo=0):
    if modo == 0:
        width = 1920
        height = 1080
    elif modo == 1:
        width = 1280
        height = 720
    elif modo == 2:
        width = 3280
        height = 2464
    else:
        print "Valor de modo no definido, usando modo=0"
        width = 1920
        height = 1080

    ima = np.zeros((height,width),dtype='int16')

    fd = open(filename,'r')
    for n in range(height):
        cad = fd.read(width*2)
        ima[n,:] = st.unpack('<%dH'%width,cad)
    fd.close()

    imagen = np.zeros((height,width,3))

    red=imagen[:,:,0]
    green=imagen[:,:,1]
    blue=imagen[:,:,2]

    red[0::2,0::2]=red[0::2,1::2]=red[1::2,0::2]=red[1::2,1::2]=ima[1::2,1::2]
    green[0::2,0::2]=green[1::2,0::2]=ima[1::2,0::2]
    green[1::2,1::2]=green[0::2,1::2]=ima[0::2,1::2]
    blue[0::2,0::2]=blue[1::2,0::2]=blue[0::2,1::2]=blue[1::2,1::2]=ima[0::2,0::2]

    return(simplest_cb(imagen, 1))

	
def procesa_raw_to_jpg( filename, fileout, modo=0):
    out = apply_percentil(filename, modo=modo)

    dst = cv2.fastNlMeansDenoisingColored(out.astype('uint8'),None,4,4,3,7)

    cv2.imwrite(fileout,(dst))
    return
