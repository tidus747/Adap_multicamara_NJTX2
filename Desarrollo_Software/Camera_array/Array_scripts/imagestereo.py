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

def calcula_estereo(imgL,imgR):
    ima_stereo = np.zeros((1080,1920,3))

    ima_stereo[270:540+270,0:960,:] = reescala_imagen(imgL,imgL.shape[1]/960.,imgL.shape[0]/540.)
    ima_stereo[270:540+270,960:,:] = reescala_imagen(imgR,imgR.shape[1]/960.,imgR.shape[0]/540.)

    return ima_stereo


if __name__ == '__main__':

    if len(sys.argv)!=3:
        print color.BOLD+'Uso:'+color.END+' debes especificar dos imagenes para calcular la imagen estereo'
        print color.DARKCYAN+'Indica la imagen izquierda y posteriormente la imagen derecha'+color.END
        sys.exit()
    # Cargamos las imagenes
    imgL = cv2.imread(sys.argv[1])
    imgR = cv2.imread(sys.argv[2])

    # Calculamos el estereo 
    ima_stereo = calcula_estereo(imgL,imgR)

    cv2.imwrite('estereo.png',(ima_stereo))
