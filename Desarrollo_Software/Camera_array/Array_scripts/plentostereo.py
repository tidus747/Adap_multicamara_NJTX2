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

import cv2
import numpy as np
import os
import sys
import scipy.misc as misc
from scipy import ndimage as ndi

class color:
    # Clase para aplicar estilos y colores al texto que mostramos en el script
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def reescala_imagen(image,w,h):
    height, width = image.shape[:2]
    res_image = cv2.resize(image,(int(width/w), int(height/h)), interpolation = cv2.INTER_CUBIC)
    return res_image

def calcula_estereo(plen):
    ima_stereo = np.zeros((1080,1920,3))
    imgL = plen[:,:,1,1,:]
    imgR = plen[:,:,1,2,:]

    ima_stereo[270:540+270,0:960,:] = reescala_imagen(imgL,imgL.shape[1]/960.,imgL.shape[0]/540.)
    ima_stereo[270:540+270,960:,:] = reescala_imagen(imgR,imgR.shape[1]/960.,imgR.shape[0]/540.)

    return ima_stereo

def checkPPM(argv):
	name = ''.join(argv)
	if (name.find('.npy') == -1):
		file = open(argv)
		if (file.readline() != "P6\n"):
			sys.exit("Wrong magic number!")
		else:
			print("PPM file confirmed!")

def readPPM(argv):
    name = ''.join(argv)
    print('Opening the plenoptic image in', name)
    if (name.find('.npy') == -1):
        checkPPM(argv)
        if (name.find('NX') != -1):
            up_L = 1+name.find('(',name.find('NX'))
            low_L = name.find(')',name.find('NX'))
            NX = int(name[up_L:low_L])
        else:
            sys.exit("Can not find NX in the filename!")
        if (name.find('NY') != -1):
            up_L = 1+name.find('(',name.find('NY'))
            low_L = name.find(')',name.find('NY'))
            NY = int(name[up_L:low_L])
        else:
            sys.exit("Can not find NY in the filename!")
        if (name.find('Nu') != -1):
            up_L = 1+name.find('(',name.find('Nu'))
            low_L = name.find(')',name.find('Nu'))
            Nu = int(name[up_L:low_L])
        else:
            sys.exit("Can not find Nu in the filename!")
        if (name.find('Nv') != -1):
            up_L = 1+name.find('(',name.find('Nv'))
            low_L = name.find(')',name.find('Nv'))
            Nv = int(name[up_L:low_L])
        else:
            sys.exit("Can not find Nv in the filename!")
        ImagePPM = ndi.imread(argv)
        plen = np.empty((NY,NX,Nv,Nu,3),dtype='uint8')
        for y in range(Nv):
            for x in range(Nu):
                plen[:,:,y,x,:] = ImagePPM[NY*y:NY*y+NY,NX*x:NX*x+NX,:]
        print("PPM image transformed to PLEN")
    else:
        plen = np.load(name)
    return plen


if __name__ == '__main__':

    if len(sys.argv)!=2:
        print color.BOLD+'Uso:'+color.END+' debes especificar la imagen plenóptica a utilizar'
        print color.DARKCYAN+'Indica la ruta y el nombre de la imagen plenóptica que se usará'+color.END
        sys.exit()
    # Cargamos las imagenes
    plen = readPPM(sys.argv[1])

    # Calculamos el estereo 
    ima_stereo = calcula_estereo(plen)

    misc.imsave("Estereo4.png",ima_stereo)
    print("Fichero escrito correctamente")
