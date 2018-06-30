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

''' Script para superponer imágenes con el uso de Gstreamer para así realizar la
calibración de las cámaras'''

import os
import sys
import textwrap
import cv2
import numpy as np

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

def genera_imagen(w,h):
   # Creamos dos "capas" para guardar la cruz
   layer1 = np.zeros((h, w, 4))
   layer2 = np.zeros((h, w, 4))

   # Definimos los colores
   red_color = (0, 0, 255, 255)
   green_color = (0, 255, 0, 255)
   blue_color = (255, 0, 0, 255)
   # Verticales
   cv2.line(layer1, (w/2,0), (w/2,(h/2)-5), blue_color, 2)
   cv2.line(layer1, (w/2,(h/2)+5), (w/2,h), blue_color, 2)

   #Horizontales
   cv2.line(layer1, (0,h/2), ((w/2)-5,h/2), blue_color, 2)
   cv2.line(layer1, ((w/2)+5,h/2), (w,h/2), blue_color, 2)

   #Centros
   cv2.rectangle(layer1, ((w/2)-3,(h/2)-3),((w/2)+3, (h/2)+3),blue_color, 1)
   #cv2.circle(layer1, (160, 120), 1, red_color, 1)
   layer1[h/2,w/2,:] = red_color

   res = layer1[:] #copy the first layer into the resulting image

   #copy only the pixels we were drawing on from the 2nd and 3rd layers
   #(if you don't do this, the black background will also be copied)
   cnd = layer2[:, :, 3] > 0
   res[cnd] = layer2[cnd]

   cv2.imwrite("rejilla.png", res)
   return

#Listado de ordenación de cámaras
cam_order = [3,0,5,1,2,4]

ancho_linea = 80
linea_punteada = color.GREEN + ancho_linea * '-' + color.END
print(linea_punteada)
print(color.BOLD + "Script para la superposición de imágenes usando Gstreamer" + color.END)
print(linea_punteada)

if len(sys.argv)!=3:
    print color.BOLD+'Uso:'+color.END+' debes especificar la cámara para superponer y la transparencia'
    print(linea_punteada)
    msg = (color.BLUE+"INFO:"+color.END+" Debes especificar cámara para superponer."
           " La transparencia que indicarás como argumento del script (valor entre 0 y 1). Como resultado, podrás"
           " observar la imagen que devuelve la cámara la superposición con la mira. Ten en cuenta, que para cerrar el programa debes cerrar"
           " antes la ventana. de no ser así puede causar problemas con Gstreamer")
    print(textwrap.fill(msg, width = ancho_linea))
    print(linea_punteada)
    print color.RED+'No has indicado los parámetros de entrada!'+color.END
    sys.exit()

genera_imagen(1280,720)

os.environ["INPUT_CAPS"] = "video/x-raw(memory:NVMM),width=(int)1920,height=(int)1080,format=(string)I420,framerate=(fraction)30/1"
os.environ["CONVERT_CAPS"] = "video/x-raw, width=(int)1280,height=(int)720,format=(string)I420,framerate=(fraction)30/1"

cam_1 = cam_order[int(sys.argv[1])]

alpha = sys.argv[2]

cmd = 'DISPLAY=:0 gst-launch-1.0 nvcamerasrc sensor-id=%d'%cam_1
cmd += ' fpsRange="30 30" ! $INPUT_CAPS ! nvvidconv ! $CONVERT_CAPS ! gdkpixbufoverlay location=rejilla.png alpha=1 ! mixer.sink_1'
cmd += ' videotestsrc pattern="black" ! video/x-raw,width=1,height=1 ! videomixer name=mixer sink_0::xpos=0 sink_0::ypos=0 sink_0::alpha=0'
cmd += ' sink_1::xpos=0 sink_1::ypos=0 ! queue ! ximagesink sync=false -v'

# Lanzamos el comando
print color.BOLD+"Comando: "+color.END,cmd
os.popen(cmd)
