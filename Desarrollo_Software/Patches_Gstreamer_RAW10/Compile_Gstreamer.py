#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from os.path import expanduser
from shutil import copyfile
from shutil import rmtree

# Definicion de clases y funciones

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

# Código principal

print(color.BLUE + "******************************************************" + color.END)
print(color.BOLD + "Script para la compilación y parcheado de Gstreamer" + color.END)
print("Iván Rodríguez Méndez")
print("Máster en Ingeniería Industrial")
print(color.PURPLE + "Universidad de la Laguna" + color.END)
print(color.BLUE + "******************************************************" + color.END)

# Guardamos la ruta donde se localiza el home
home = expanduser("~") # Guardamos la ruta home del usuario
dir_exec = os.path.abspath(os.path.dirname(sys.argv[0])) # Guardamos la ruta donde está el script
PATCH_NAME = "0001-GstreamerRAW10-modify.patch"

# Definimos las variables de entorno que usaremos
VERSION='1.8.0'

# Creamos una carpeta en la que almacenaremmos el código fuente

# TODO Se podría introducir todo este fragmento en una función para poder llamarlo cada
# vez que intentamos crear un directorio y necesitamos saber si borrar su contenido
if not os.path.exists(home+"/gst_"+VERSION): # Comprobamos si está creada con anterioridad
    os.makedirs(home+"/gst_"+VERSION)
    print("Creado el directorio "+ color.GREEN + home+"/gst_"+VERSION + color.END)
else:
    respuesta = raw_input("¿Desea " + color.BOLD + "borrar" + color.END + " el directorio "+ home+"/gst_"+VERSION+ "? S/N")
    if respuesta == "S" or respuesta == "s":
        print("Eliminado el directorio "+ color.RED + home+"/gst_"+VERSION + color.END)
        rmtree(home+"/gst_"+VERSION, ignore_errors=True)
        os.makedirs(home+"/gst_"+VERSION)
        print("Creado el directorio "+ color.GREEN + home+"/gst_"+VERSION + color.END)
    else:
        print("Conservamos el directorio "+ color.GREEN + home+"/gst_"+VERSION + color.END)

# Una vez creado el directorio nos movemos hasta él
os.chdir(home+"/gst_"+VERSION)

# Comenzamos a descargar el código fuente que necesitamos

# TODO Estamos descargando todos los paquetes de Gstreamer aunque realmente solo nos hace Falta
# el paquete gst-plugins-good. Se podría implementar la posibilidad de preguntarle al usuario

# TODO Hay que crear una función para comprobar si los ficheros ya están descargados y en caso
# contrario que sean descargados. Si los ficheros ya están descargados existe el problema de que
# se crean copias de los mismos.

print("Descargando..."+ color.BLUE + "gst-plugins-base-"+VERSION + color.END)
os.system("wget https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-"+VERSION+".tar.xz --no-check-certificate")
print("Descargando..."+ color.BLUE + "gstreamer-"+VERSION + color.END)
os.system("wget https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-"+VERSION+".tar.xz --no-check-certificate")
print("Descargando..."+ color.BLUE + "gst-plugins-ugly-"+VERSION + color.END)
os.system("wget https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-"+VERSION+".tar.xz --no-check-certificate")
print("Descargando..."+ color.BLUE + "gst-plugins-good-"+VERSION + color.END)
os.system("wget https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-"+VERSION+".tar.xz --no-check-certificate")
print("Descargando..."+ color.BLUE + "gst-plugins-bad-"+VERSION + color.END)
os.system("wget https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-"+VERSION+".tar.xz --no-check-certificate")

print(color.BOLD + "Se han descargado todos los paquetes"+ color.END)

# Descomprimimos los ficheros que hemos descargado en el directorio actual
print(color.YELLOW + "Descomprimiendo los ficheros descargados ..."+ color.END)
os.system("for a in `ls -1 *.tar.*`; do tar -xf $a; done")
print(color.YELLOW + "¡Ficheros descomprimidos!"+ color.END)

# Instalamos las dependencias que necesita el sistema
print(color.BLUE +"Instalando dependencias del sistema..."+ color.END)
os.system("sudo apt-get install build-essential dpkg-dev flex bison autotools-dev automake \
autopoint libtool gtk-doc-tools libgstreamer1.0-dev \
libxv-dev libasound2-dev libtheora-dev libogg-dev libvorbis-dev \
libbz2-dev libv4l-dev libvpx-dev libjack-jackd2-dev libsoup2.4-dev libpulse-dev \
faad libfaad-dev libgl1-mesa-dev libgles2-mesa-dev \
libx264-dev libmad0-dev")
print(color.BLUE + "¡Dependencias instaladas!" + color.END)

# TODO hay que tratar de que todas las sentencias sean con un try/catch
print(color.YELLOW + "Importando el parche..." + color.END)
os.system("quilt import "+dir_exec+"/"+PATCH_NAME)
print(color.YELLOW + "¡Parche importado!" + color.END)

print(color.YELLOW + "Cargando el parche..." + color.END)
os.system("quilt push -a")
print(color.YELLOW + "¡Parche cargado!" + color.END)

# Ahora pasamos a compilar el parche que hemos creado
print(color.YELLOW + "Recompilando gst-plugins-good-"+VERSION + color.END)
print(color.PURPLE + "Entrando en el directorio...gst-plugins-good-"+VERSION+ color.END)
os.chdir("gst-plugins-good-"+VERSION)
os.system("./configure --prefix="+home+"/gst_"+VERSION+"/out")
os.system("time make")
os.system("make install")
