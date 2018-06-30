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

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import rawread as rr
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

def test_modes_cam(cam):
    cad = 'v4l2-compliance -d /dev/video%d'%cam
    cad += ' | grep Total:'
    cad += " | cut -d ',' -f 2"
    cad += " | cut -d ':' -f 2"
    a = int(os.popen(cad).read())
    return(a)

Pinta = True
lcam = []
for cam in range(6):
    succeed = test_modes_cam(cam)
    if(succeed == 42):
        lcam.append(cam)

print u" Lista de cámaras disponibles",lcam


def take_view(cam, modo = 0):
    if modo == 0:
        fmt = [1920,1080,'RG10']
    elif modo == 1:
        fmt = [1280,720,'RG10']
    elif modo == 2:
        fmt = [3280,2464,'RG10']
    else:
        print "take_view - Error: modo desconocido"
        return

    cad = '~/src/Setup_Auvidea_J20/GPIO_Reset.sh'
    print "comando: ",cad
    a = os.popen(cad).read()

    cad = 'v4l2-ctl -d /dev/video%d '%cam
    # fmt = [int,int,char] = [ancho, alto, pixelformat]
    cad += '--set-fmt-video=width=%d,height=%d,pixelformat=%s '%(fmt[0],fmt[1],fmt[2])
    cad += '--set-ctrl bypass_mode=0,gain=4000,coarse_time=60000,'
    cad += 'hdr_enable=1  --stream-mmap --stream-count=1 '
    cad += '--stream-to=capture_camara_%d.raw'%cam
    print "comando: ",cad
    a = os.popen(cad).read()
    print "retorno: ",a
    return


if len(sys.argv)!=2:
    print 'Uso: dime el nombre de salida de las imagenes'
    sys.exit()

modo = 0

for camact in lcam:
    take_view(camact, modo=modo)

list_cam_dev = np.array([2, 5, 0, 4, 3, 1])
fileout = sys.argv[1]
for camact in lcam:
    filename = 'capture_camara_%d.raw'%camact
    fileout = 'CAM%d_'%list_cam_dev[camact]+sys.argv[1]+'.jpg'
    rr.procesa_raw_to_jpg( filename, fileout, modo=modo)

if (Pinta == True):
    Camera_images = []
    for i in range(len(lcam)):
        Camera_images.append(sorted(glob.glob('./CAM'+str(i)+'_'+sys.argv[1]+'.jpg'),key = lambda x: x.split("_")))

plt.figure(1)
plt.subplot(231)
imagen = cv2.imread(Camera_images[0][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM0')
plt.subplot(232)
imagen = cv2.imread(Camera_images[1][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM1')
plt.subplot(233)
imagen = cv2.imread(Camera_images[2][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM2')
plt.subplot(234)
imagen = cv2.imread(Camera_images[3][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM3')
plt.subplot(235)
imagen = cv2.imread(Camera_images[4][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM4')
plt.subplot(236)
imagen = cv2.imread(Camera_images[5][0])
plt.imshow(imagen[:,:,[2,1,0]])
plt.title('CAM5')

plt.figure(2)
imagen_0 = cv2.imread(Camera_images[0][0])
imagen_1 = cv2.imread(Camera_images[1][0])
imagen_2 = cv2.imread(Camera_images[2][0])
imagen_3 = cv2.imread(Camera_images[3][0])
imagen_4 = cv2.imread(Camera_images[4][0])
imagen_5 = cv2.imread(Camera_images[5][0])
imagen_arriba = (imagen_0.astype('float')+imagen_1.astype('float')+imagen_2.astype('float'))/3.
imagen_abajo = (imagen_3.astype('float')+imagen_4.astype('float')+imagen_5.astype('float'))/3.
plt.subplot(211)
plt.imshow(imagen_arriba[:,:,[2,1,0]].astype('uint8'))
plt.title(u'Suma de imágenes superiores')
plt.subplot(212)
plt.imshow(imagen_abajo[:,:,[2,1,0]].astype('uint8'))
plt.title(u'Suma de imágenes inferiores')

plt.show()
