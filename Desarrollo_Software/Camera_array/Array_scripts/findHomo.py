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


if len(sys.argv)!=3:
    print(u"Número de parámetros de entrada incorrecto.")
    print(u"Uso: "+sys.argv[0]+" <path>")
    sys.exit()


camarr = CamArray()
calibfile = open("calfile.cbf","r")
camarr.read(calibfile)
calibfile.close()

camarr.calHomo(sys.argv[1],sys.argv[2])

calibfile = open(sys.argv[1]+"calfile.cbf","w")
camarr.write(calibfile)
calibfile.close()

print(u"Homografías escritas en el fichero calfile.cbf")
