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

import numpy as np
import busca_chessboard as bc
import cv2
from matplotlib import pyplot as plt
import struct as st

class Camara:
	"""Clase para manejar una cámara"""
	def __init__(self,mtx=np.array([[1.,0,0.],[0.,1.,0.],[0,0,1]]),dist=np.zeros(5),tam_pix=2e-3,tam_cuadrado=28.):
		self.mtx=mtx# Camera matrix
		self.dist=dist # Distortion parameters
		self.rvecs=[]# Rotation pose
		self.tvecs=[]# Translation pose
		self.Rt=[] # Lista para almacenar todas las matrices de rotación y traslación de las vistas
		#self.Hw=np.zeros((3,4)) # Camera transform world to image (no distortion included)
		#self.H=np.zeros((3,3))  # Homography to central camera (array definition TODO)
		self.corners = []
		self.tam_pix = tam_pix
		self.tam_cuadrado = tam_cuadrado
		self.image_h = 1080
		self.image_w = 1920
		self.Ncx = 9
		self.Ncy = 6
		self.h = self.image_h*self.tam_pix/self.tam_cuadrado
		self.w = self.image_w*self.tam_pix/self.tam_cuadrado
		self.focal = np.mean((self.mtx[0,0],self.mtx[1,1]))*self.tam_pix/self.tam_cuadrado
		self.err = ''
		return

	def parametros(self):
		self.h = self.image_h*self.tam_pix/self.tam_cuadrado
		self.w = self.image_w*self.tam_pix/self.tam_cuadrado
		self.focal = np.mean((self.mtx[0,0],self.mtx[1,1]))*self.tam_pix/self.tam_cuadrado
		return

	def __str__(self):
		pac='\nCamera matrix:\n'
		for nn in range(self.mtx.shape[0]):
			for mm in range(self.mtx.shape[1]):
				pac+='%f '%(self.mtx[nn,mm])
			pac += '\n'
		pac+='\nDistortion:\n'
		pac+='%02d\n' %(self.dist.shape[0])
		for nn in range(self.dist.shape[0]):
			pac+='%f ' %(self.dist[nn])
		return pac

	def add_vistas(self,**params):
		# Función para agregar varias vistas a nuestra cámara
		if params.has_key('tvecs') and params.has_key('rvecs'):
			# Los parámetros introducidos son correctos
			if (len(params['tvecs'])==len(params['rvecs'])):
				# Una vez comprobado que las listas son iguales, guardamos las vistas
				for i in range(len(params['tvecs'])):
					Rt = np.zeros((3,4))
					Rt[:,0:3] = cv2.Rodrigues(params['rvecs'][i])[0]
					Rt[:,3:] = params['tvecs'][i]

					self.Rt.append(Rt)
					#self.Hw=np.dot(self.mtx,self.Rt)
					self.tvecs.append(params['tvecs'][i])
					self.rvecs.append(params['rvecs'][i])
			else:
				self.err = u"ERROR en add_vistas(): Dimensiones de parámetros distintas"
				return
		else:
			self.err = u"ERROR en add_vistas(): Parámetros de entrada no vaĺidos"
			return
		return

	def calibrate(self,filenames,img_frontal):

		# Calculamos los puntos del mundo
		objp = bc.genera_coordenadas(self.Ncx,self.Ncy)

		objpoints = []
		imgpoints = []

		for filename in filenames:
			print("Calibrando "+filename)

			imagen = cv2.imread(filename)

			corners, ret = bc.busca_chessboard(imagen, self.Ncx, self.Ncy)

			if (ret == True):
				objpoints.append(objp)
				imgpoints.append(corners)

				mtx = np.zeros((3,3))
				mtx[0,0] = 1520.
				mtx[0,2] = self.image_w/2.
				mtx[1,1] = 1520.
				mtx[1,2] = self.image_h/2.
				mtx[2,2] = 1

				if (len(self.rvecs)==0 or len(self.tvecs)==0):
					ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, imagen.shape[1::-1],cameraMatrix = mtx, distCoeffs=self.dist,flags=cv2.CALIB_FIX_ASPECT_RATIO )
				else:
					ret, mtx, dist, rvec, tvec = cv2.calibrateCamera(objpoints, imgpoints, imagen.shape[1::-1],cameraMatrix=mtx, distCoeffs=self.dist,rvecs= self.rvecs,tvecs=self.tvecs, flags=cv2.CALIB_FIX_ASPECT_RATIO )

				self.mtx = mtx
				self.dist = dist

				# Guardamos los datos que se han generado
				for i in range(len(rvec)):
					Rt = np.zeros((3,4))
					Rt[:,0:3] = cv2.Rodrigues(rvec[i])[0]
					Rt[:,3:] = tvec[i]

					self.Rt.append(Rt)
					self.tvecs.append(tvec[i])
					self.rvecs.append(rvec[i])


			imagen = cv2.imread(img_frontal)
			imagen_undistort = cv2.undistort(imagen, self.mtx, self.dist, None)

			# TODO Hay imágenes que salen con una distorsión lateral demasiado grande como para detectar corners
			corners, ret = bc.busca_chessboard(imagen_undistort, self.Ncx, self.Ncy)
			self.corners = corners

		return



	def pinta(self,nvis= -1, axis3D = -1, Name = ''):
		if(nvis>len(self.Rt)):
			self.err = u"ERROR en pinta(): Parámetros de entrada no válidos"
			return

		if (axis3D == -1):
			fig = plt.figure()
			ax = fig.add_subplot(111, projection='3d')
		else:
			ax = axis3D

        # Generamos las coordenadas de los puntos del mundo (tablero)
        # TODO Analizar si la mejor forma de generar los puntos es importando el módulo o debemos generarlos
        # de otra forma
		objp = bc.genera_coordenadas(9,6)
        # Generamos las variables para pode representar la cámara en el espacio
		pt_cam=np.zeros((5,3))

		self.parametros() # Volvemos a calcular los parámetros de la cámara

		# Establecemos las coordenadas de la cámara
		pt_cam[0] = [self.mtx[0,2]*self.tam_pix/self.tam_cuadrado,self.mtx[1,2]*self.tam_pix/self.tam_cuadrado,0 ]
		pt_cam[1] = [0,self.h,self.focal]
		pt_cam[2] = [self.w,self.h,self.focal]
		pt_cam[3] = [self.w,0,self.focal]
		pt_cam[4] = [0,0,self.focal]
		# Construimos los puntos para su representación
		x = [pt_cam[0,0],pt_cam[1,0],np.nan,pt_cam[0,0],pt_cam[2,0],np.nan,pt_cam[0,0],pt_cam[3,0],np.nan]
		x += [pt_cam[0,0],pt_cam[4,0],pt_cam[1,0],pt_cam[2,0],pt_cam[3,0],pt_cam[4,0]]
		y = [pt_cam[0,1],pt_cam[1,1],np.nan,pt_cam[0,1],pt_cam[2,1],np.nan,pt_cam[0,1],pt_cam[3,1],np.nan]
		y += [pt_cam[0,1],pt_cam[4,1],pt_cam[1,1],pt_cam[2,1],pt_cam[3,1],pt_cam[4,1]]
		z = [pt_cam[0,2],pt_cam[1,2],np.nan,pt_cam[0,2],pt_cam[2,2],np.nan,pt_cam[0,2],pt_cam[3,2],np.nan]
		z += [pt_cam[0,2],pt_cam[4,2],pt_cam[1,2],pt_cam[2,2],pt_cam[3,2],pt_cam[4,2]]

		# Guardamos los puntos es una matriz
		xyz = np.ones((4,len(x)))
		xyz[0,:] = x
		xyz[1,:] = y
		xyz[2,:] = z

		# Representamos los puntos del mundo
		ax.plot(objp[:,:,0].reshape(54,),objp[:,:,1].reshape(54,),objp[:,:,2].reshape(54,),'ro')

		if(nvis == -1):
			# Si nvis es igual a -1 representaremos todas las imágenes
			for i in range(len(self.Rt)):
				xyz_mod=np.dot(self.Rt[i],xyz)
				ax.plot(xyz_mod[0,:],xyz_mod[1,:],xyz_mod[2,:])
				ax.text(xyz_mod[0,0],xyz_mod[1,0],xyz_mod[2,0], Name+" Vista_"+str(i), color='red')
		else:
			xyz_mod=np.dot(self.Rt[nvis],xyz)
			ax.plot(xyz_mod[0,:],xyz_mod[1,:],xyz_mod[2,:])
			ax.text(xyz_mod[0,0],xyz_mod[1,0],xyz_mod[2,0], Name+" Vista_"+str(nvis), color='red')

		ax.set_xlabel('Eje X')
		ax.set_ylabel('Eje Y')
		ax.set_zlabel('Eje Z')

		if (axis3D == -1):
			plt.show()
		return

	def write(self,filename):
		for i in range(3):
			for j in range(3):
				pac=st.pack('<d',self.mtx[i,j])
				filename.write(pac)

		for i in range(5):
			pac=st.pack('<d',self.dist[i])
			filename.write(pac)


		return

	def read(self,filename):
		for i in range(3):
			for j in range(3):
				self.mtx[i,j]=st.unpack('<d',filename.read(8))[0]
				print(u"Matriz de Cámara[%d,%d]: %f"%(i,j,self.mtx[i,j]))

		for i in range(5):
			self.dist[i] = st.unpack('<d',filename.read(8))[0]
			print(u"Distorsión[%d]: %f"%(i,self.dist[i]))

		return
