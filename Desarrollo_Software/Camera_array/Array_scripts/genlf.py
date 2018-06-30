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

import sys
from CamArray import CamArray
import cv2
import busca_chessboard as bc
from matplotlib import pyplot as plt
import glob
import numpy as np
import scipy.misc as misc


if len(sys.argv)!=2:
    print(u"Número de parámetros de entrada incorrecto.")
    print(u"Uso: "+sys.argv[0]+" <path>")
    sys.exit()

camarr = CamArray()

calibfile = open(sys.argv[1]+"calfile.cbf","r")
camarr.read(calibfile)
calibfile.close()

print(u"Parámetros de calibración leídos desde el fichero calfile.cbf")

dirname = sys.argv[1]

Camera_images = (sorted(glob.glob(dirname+'CAM?_*'),key = lambda x: x.split("_")))

imagen = cv2.imread(Camera_images[0])
lf = np.zeros((imagen.shape[0]*camarr.h,imagen.shape[1]*camarr.w,3))
plen = np.zeros((imagen.shape[0],imagen.shape[1],camarr.h,camarr.w,3),dtype='uint8')
image_plen = np.zeros((imagen.shape[0]*camarr.h,imagen.shape[1]*camarr.w,3),dtype='uint8')

i=0
print(u"Procesando imágenes para generar el LF...")
for nv in range(camarr.h):
    for nu in range(camarr.w):
        print(u"Procesando... "+ Camera_images[i])

        imagen = cv2.imread(Camera_images[i])

        mtx = camarr.camarr[nv][nu].mtx
        distcoef = camarr.camarr[nv][nu].dist

        undistort = cv2.undistort(imagen, mtx, distcoef, None)

        plen[:,:,nv,nu,:] = cv2.warpPerspective(undistort,camarr.homo[nv][nu],(imagen.shape[1],imagen.shape[0]), flags=cv2.WARP_INVERSE_MAP)

        image_plen[nv*imagen.shape[0]:(nv*imagen.shape[0])+imagen.shape[0],nu*imagen.shape[1]:(nu*imagen.shape[1])+imagen.shape[1],:] = plen[:,:,nv,nu,:]

        i += 1

name = "plen-NX(%d)-NY(%d)-Nu(0%d)-Nv(0%d).reversed"%(imagen.shape[1],imagen.shape[0],camarr.w,camarr.h)
filename = dirname+name
misc.imsave(filename+".ppm",image_plen[:,:,[2,1,0]])
print(u"Imagen guardada en ... "+filename+".ppm")
np.save(filename+".npy",plen)
print(u"Array numpy guardado en... "+filename+".npy")
