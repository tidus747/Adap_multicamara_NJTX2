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
import scipy.signal as sig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

NORMAL = 0
ADV_X  = 1
ADV_Y  = 2

def dist2(p,q, mode=NORMAL):
	dx=(p[0]-q[0])**2
	dy=(p[1]-q[1])**2
	if mode == NORMAL:
		return(np.sqrt(dx+dy))
	elif mode == ADV_X:
		return(np.sqrt(dx+dy*10))
	elif mode == ADV_Y:
		return(np.sqrt(dx*10+dy))
	else:
		pass
	print "dist2: error, modo no válido"
	return(np.inf)


def dist(p, corn, mode=NORMAL):
	indpto = None
	dmin = np.inf
	for n in range(len(corn)):
		d = dist2(p,corn[n], mode)
		if(d < dmin):
			dmin = d
			indpto = n

	return (dmin, indpto)

def busca_chessboard(img,Ncx,Ncy):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	(h,w) = gray.shape

	# Esto es el kernel para localizar las esquinas de los cuadrados
	# TODO ver la relación entre la detección y el tamaño del kernel
	tam=15
	fil1=np.concatenate((np.ones((tam,tam)),-1*np.ones((tam,tam))))
	kernel = np.concatenate((fil1*-1,fil1),axis=1)

	mask = cv2.filter2D(gray, cv2.CV_32F, np.ones((55,55))/(55*55.))

	# Hacemos la convolución esperando que los máximos y los mínimos
	# sean las esquinas del tablero en una curiosa organización dameril.
	aver=sig.convolve2d((gray<mask).astype('float'),kernel,'same').astype('int')

	# Generamos las imágenes coordenadas para ayudar a localizar los
	# puntos ordenados.
	otra=aver.reshape(h*w)
	ind = otra.argsort()

	corn=[]
	n=0
	while (len(corn)<27):
		p=[ind[n]%w,ind[n]//w]
		dmin, indpto = dist(p,corn)
		if  dmin > 10:
			corn.append(p)
		n+=1

	n=-1
	while (len(corn)<54):
		p=[ind[n]%w,ind[n]//w]
		dmin, indpto = dist(p,corn)
		if dmin > 10:
			corn.append(p)
		n-=1

	corn=np.array(corn)

	corners = []
	# Buscamos el primer punto como el más cercano a la esquina inferior izquierda
	esq_inf_izq = np.array([0,1080])
	dmin, indpto = dist(esq_inf_izq, corn)
	corners.append(corn[indpto])
	corn=np.concatenate((corn[:indpto], corn[indpto+1:]))

	for n in range(5):
		for n in range(8):
			dmin, indpto = dist(corners[-1], corn, mode=ADV_X)
			corners.append(corn[indpto])
			corn=np.concatenate((corn[:indpto], corn[indpto+1:]))

		dmin, indpto = dist(corners[-9], corn, mode=ADV_Y)
		corners.append(corn[indpto])
		corn=np.concatenate((corn[:indpto], corn[indpto+1:]))
	for n in range(8):
		dmin, indpto = dist(corners[-1], corn, mode=ADV_X)
		corners.append(corn[indpto])
		corn=np.concatenate((corn[:indpto], corn[indpto+1:]))
	corners = np.array(corners,dtype='float32')

	paso = corners.reshape(6,9,2)

	dx=np.diff(paso[:,:,0],axis=1)
	dxm=np.mean(dx)
	dy=np.diff(paso[:,:,1],axis=0)
	dym=np.mean(dy)
	ret = True
	ret = ret and np.logical_and(dx>(dxm-0.2*dxm),dx<(dxm+0.2*dxm)).all()
	ret = ret and np.logical_and(dy>(dym+0.2*dym),dy<(dym-0.2*dym)).all()
	return corners, ret

def pinta_chessboard(img, corn, mode='or'):
	plt.imshow(img[:,:,[2,1,0]])
	#plt.plot((corn[:,0]+1)*img.shape[1]/2,(corn[:,1]+1)*img.shape[0]/2,mode)
	plt.plot(corn[:,0],corn[:,1],mode)
	for n in range(len(corn)):
		plt.text(corn[n,0]+10,corn[n,1]+10,'%d'%n, fontsize=12, bbox=dict(facecolor='red', alpha=0.5))
	plt.show()

	return

def genera_coordenadas(puntosx,puntosy):
	# Generamos los puntos del mundo
	coordenadas = []
	for py in range(puntosy):
		for px in range(puntosx):
			coordenadas.append([puntosx-px,py,0])
	return np.array([coordenadas],dtype='float32')

def proyecta_punto(mtx,rvecs,tvecs,dst,puntos_objeto):
	# Función para generar la proyección de un punto con distorsión
	Rt = np.zeros((3,4))
	#TODO hay que tener en cuenta la vista que queremos transformar, por ahora trabajamos
	# con la vista frontal
	Rt[:,0:3] = cv2.Rodrigues(rvecs[2])[0]
	Rt[:,3:] = tvecs[2]
	xyz=np.dot(Rt,puntos_objeto)

	# Calculamos los puntos de la imagen
	x_prim = np.zeros((1,xyz.shape[1]))
	y_prim = np.zeros((1,xyz.shape[1]))

	x_prim = xyz[0,:]/xyz[2,:]
	y_prim = xyz[1,:]/xyz[2,:]

	# Asignamos las distorsiones

	k1 = dst[0,0]
	k2 = dst[0,1]
	p1 = dst[0,2]
	p2 = dst[0,3]
	k3 = dst[0,4]

	# Calculamos las x_prim2 e y_prim2
	r_2 = x_prim**2 + y_prim**2

	x_prim2 = x_prim*(1+k1*r_2+k2*r_2**2+k3*r_2**3)+2*p1*x_prim*y_prim+p2*(r_2+2*x_prim**2)
	y_prim2 = y_prim*(1+k1*r_2+k2*r_2**2+k3*r_2**3)+p1*(r_2+2*y_prim**2)+2*p2*x_prim*y_prim

	px_imagen = mtx[0,0]*x_prim2+mtx[0,2]
	py_imagen = mtx[1,1]*x_prim2+mtx[1,2]

	return px_imagen,py_imagen

def proyecta_punto_no_dist(mtx,rvecs,tvecs,puntos_objeto):
	# Función para generar la proyección de un punto sin distorsión
	Rt = np.zeros((3,4))
	#TODO hay que tener en cuenta la vista que queremos transformar, por ahora trabajamos
	# con la vista frontal
	Rt[:,0:3] = cv2.Rodrigues(rvecs[2])[0]
	Rt[:,3:] = tvecs[2]
	xyz=np.dot(mtx,np.dot(Rt,puntos_objeto))

	# Calculamos los puntos de la imagen
	x_prim = np.zeros((1,xyz.shape[1]))
	y_prim = np.zeros((1,xyz.shape[1]))

	x_prim = xyz[0,:]/xyz[2,:]
	y_prim = xyz[1,:]/xyz[2,:]
	return x_prim,y_prim

def calib_cam(ncam,Ncx,Ncy):
	u"""Función para la calibración de una cámara"""
	# Lista de nombres de las vistas de calibracion.
	nomcam=['abajo', 'izquierda', 'frontal', 'derecha', 'arriba']

	# Generamos los puntos de la rejilla en el mundo
	objp = genera_coordenadas(Ncx,Ncy)

	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane
	for nvis in range(5):
		filename = nomcam[nvis]+'_%d.jpg'%ncam
		img = cv2.imread(filename)
		corners, ret = busca_chessboard(img, Ncx, Ncy)
		if(ret == False):
			print "La imagen %s dio una mala detección\n"%(filename)
			return
		objpoints.append(objp)
		imgpoints.append(corners)

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1],None,None)

	return mtx, dist, rvecs, tvecs

def representa_pose(mtx,tvecs, rvecs):
	u"""Función para la representación de la pose de una cámara"""
	nomcam=['abajo', 'izquierda', 'frontal', 'derecha', 'arriba']

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	objp = genera_coordenadas(9,6)
	pt_cam=np.zeros((5,3))
	tam_pix = 2e-3
	h = 1080*tam_pix/28.
	w = 1920*tam_pix/28.
	focal = np.mean((mtx[0,0],mtx[1,1]))*tam_pix/28.

	pt_cam[0] = [mtx[0,2]*tam_pix/28.,mtx[1,2]*tam_pix/28.,0 ]
	pt_cam[1] = [0,h,focal]
	pt_cam[2] = [w,h,focal]
	pt_cam[3] = [w,0,focal]
	pt_cam[4] = [0,0,focal]

	x = [pt_cam[0,0],pt_cam[1,0],np.nan,pt_cam[0,0],pt_cam[2,0],np.nan,pt_cam[0,0],pt_cam[3,0],np.nan]
	x += [pt_cam[0,0],pt_cam[4,0],pt_cam[1,0],pt_cam[2,0],pt_cam[3,0],pt_cam[4,0]]
	y = [pt_cam[0,1],pt_cam[1,1],np.nan,pt_cam[0,1],pt_cam[2,1],np.nan,pt_cam[0,1],pt_cam[3,1],np.nan]
	y += [pt_cam[0,1],pt_cam[4,1],pt_cam[1,1],pt_cam[2,1],pt_cam[3,1],pt_cam[4,1]]
	z = [pt_cam[0,2],pt_cam[1,2],np.nan,pt_cam[0,2],pt_cam[2,2],np.nan,pt_cam[0,2],pt_cam[3,2],np.nan]
	z += [pt_cam[0,2],pt_cam[4,2],pt_cam[1,2],pt_cam[2,2],pt_cam[3,2],pt_cam[4,2]]

	xyz = np.ones((4,len(x)))
	xyz[0,:] = x
	xyz[1,:] = y
	xyz[2,:] = z

	Rt = np.zeros((3,4))
	ax.plot(objp[:,:,0].reshape(54,),objp[:,:,1].reshape(54,),objp[:,:,2].reshape(54,))
	for i in range(len(tvecs)):
		Rt[:,0:3] = cv2.Rodrigues(rvecs[i])[0]
		Rt[:,3:] = tvecs[i]
		xyz_mod=np.dot(Rt,xyz)
		ax.plot(xyz_mod[0,:],xyz_mod[1,:],xyz_mod[2,:])
		ax.text(np.asscalar(tvecs[i][0]), np.asscalar(tvecs[i][1]),np.asscalar(tvecs[i][2]), nomcam[i], color='red')
	ax.set_xlabel('Eje X')
	ax.set_ylabel('Eje Y')
	ax.set_zlabel('Eje Z')
	plt.show()

	return

def representa_camaras(tvecs, rvecs):
	u"""Función para la representación de la pose de un array de cámaras"""
	# La entrada a esta función serán los tvecs (np.array) y los rvecs de todas las cámaras, unidos por columnas

	nomcam=['abajo', 'izquierda', 'frontal', 'derecha', 'arriba']

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	objp = genera_coordenadas(9,6)
	ax.scatter(objp[:,:,0], objp[:,:,1],objp[:,:,2],color='b',marker='o')
	# TODO Hay que revisar las direcciones de los rvecs para así calcular el apuntado de la cámara

	for cam in range(tvecs.shape[2]):
		for i in range(len(tvecs)):
			ax.scatter(tvecs[i,cam][0], tvecs[i,cam][1], tvecs[i,cam][2],color='r',marker='*')
			cad = nomcam[i]+'_%d'%cam
			ax.text(tvecs[i,cam][0], tvecs[i,cam][1],tvecs[i,cam][2], cad, color='red')

	ax.set_xlabel('Eje X')
	ax.set_ylabel('Eje Y')
	ax.set_zlabel('Eje Z')
	plt.show()
