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
import glob
from camara import Camara as Camera
import cv2
import struct as st
import numpy as np
import busca_chessboard as bc

def sort_camfiles(dirname,numCameras=6,nvis_front="01", nvis_calib = "*"):
    Camera_front = []
    Camera_calib =[]
    for i in range(numCameras):
        Camera_front.append(sorted(glob.glob(dirname+'CAM'+str(i)+'_'+nvis_front+'.jpg'),key = lambda x: x.split("_")))
        Camera_calib.append(sorted(glob.glob(dirname+'CAM'+str(i)+'_'+nvis_calib+'.jpg'),key = lambda x: x.split("_")))
    return Camera_front, Camera_calib


class CamArray:
	"""Clase para manejar un array de cámaras"""
	def __init__(self,w=None,h=None):
		self.w= 3 # Ancho del array
		self.h= 2# Alto del array
		# Generación de una lista de dos dimensiones
		camera_array = []
		for j in range(self.h):
                    nx = []
                    for i in range(self.w):
                        nx.append(0)
                        camera_array.append(nx)
                self.camarr=camera_array # Lista para almacenar las cámaras
                self.homo = [i[:] for i in camera_array] # Creamos una copia de la lista para las homografías
                return

        def calibrate(self,dirname):
            Camera_front, Camera_calib = sort_camfiles(dirname)

            cam00 = Camera()
            cam00.calibrate(Camera_calib[4],Camera_front[4][0]) # Calibramos la cámara central inferior, será la referencia

            i = 0
            for nv in range(self.h):
                for nu in range(self.w):
                    self.camarr[nv][nu] = Camera()
                    self.camarr[nv][nu].calibrate(Camera_calib[i],Camera_front[i][0])

                    retval, mask = cv2.findHomography(self.camarr[nv][nu].corners,cam00.corners)
                    self.homo[nv][nu] = retval

                    i+=1

            return

        def calHomo(self,dirname,filename):
            Camera_homo = (sorted(glob.glob(dirname+'CAM*_'+filename+'.jpg'),key = lambda x: x.split("_")))

            # Corners de la imagen de referencia
            imagen = cv2.imread(Camera_homo[4])
            imagen_undistort = cv2.undistort(imagen, self.camarr[1][1].mtx, self.camarr[1][1].dist, None)
            corners, ret = bc.busca_chessboard(imagen_undistort, self.camarr[1][1].Ncx, self.camarr[1][1].Ncy)

            if (ret == True):
                self.camarr[1][1].corners = corners
            else:
                print(u"No se han calculado los corners en la imagen "+Camera_homo[4])

            i = 0
            for nv in range(self.h):
                for nu in range(self.w):
                    print("Calibrando "+Camera_homo[i])
                    imagen = cv2.imread(Camera_homo[i])
                    imagen_undistort = cv2.undistort(imagen, self.camarr[nv][nu].mtx, self.camarr[nv][nu].dist, None)
                    corners, ret = bc.busca_chessboard(imagen_undistort, self.camarr[nv][nu].Ncx, self.camarr[nv][nu].Ncy)
                    if (ret == True):
                        self.camarr[nv][nu].corners = corners
                        retval, mask = cv2.findHomography(self.camarr[nv][nu].corners,self.camarr[1][1].corners, cv2.RANSAC)
                        self.homo[nv][nu] = retval
                    else:
                        print(u"No se han calculado los corners en la imagen "+Camera_homo[i])
                    i+=1

            return


        def write(self,filename):
            filename.write(st.pack('<i',self.w))
            filename.write(st.pack('<i',self.h))
            for nv in range(self.h):
                for nu in range(self.w):
                    self.camarr[nv][nu].write(filename)

                    for i in range(3):
                        for j in range(3):
                            filename.write(st.pack('<d',self.homo[nv][nu][i,j]))
            return

        def read(self, filename):
            self.w = st.unpack('<i',filename.read(4))[0]
            print("w: %d"%self.w)
            self.h = st.unpack('<i',filename.read(4))[0]
            print("h: %d"%self.h)

            for nv in range(self.h):
                for nu in range(self.w):
                    self.camarr[nv][nu] = Camera()
                    print(u"Cámara[%d][%d]"%(nv,nu))

                    self.camarr[nv][nu].read(filename)
                    self.homo[nv][nu] = np.zeros((3,3),dtype='float')

                    for i in range(3):
                        for j in range(3):
                            self.homo[nv][nu][i,j] = st.unpack('<d',filename.read(8))[0]
                            print(u"Homografía[%d][%d]: %f"%(i,j,self.homo[nv][nu][i,j]))

            return
