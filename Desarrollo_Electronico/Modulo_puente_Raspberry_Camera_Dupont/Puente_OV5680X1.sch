EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:switches
LIBS:relays
LIBS:motors
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:qth-060-01-h-d-a
LIBS:Puente_OV5680X1-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "Módulo Puente para sensor OV5640 y Nvidia Jetson TX2"
Date "2018-02-12"
Rev "1.0"
Comp "Universidad de la Laguna"
Comment1 "Iván Rodríguez Méndez"
Comment2 "Adaptación multicámara NVIDIA JETSON TX2"
Comment3 "Área de Teoría de la Señal y Comunicación"
Comment4 "Departamento de Ingeniería Industrial"
$EndDescr
Text Notes 2015 4675 0    60   ~ 0
Pines procedentes del módulo de depuración\n\n
$Comp
L Conn_01x30 J5
U 1 1 5A8347D5
P 5530 2555
F 0 "J5" H 5530 4055 50  0000 C CNN
F 1 "Conn_01x30" H 5530 955 50  0000 C CNN
F 2 "I-PEX-30:SOIC-30-MOD" H 5530 2555 50  0001 C CNN
F 3 "" H 5530 2555 50  0001 C CNN
	1    5530 2555
	1    0    0    1   
$EndComp
Text Notes 4735 4620 0    60   ~ 0
Conector al módulo de cámara\n
Text GLabel 5330 3955 0    39   Input ~ 0
GND
Text GLabel 5330 3655 0    39   Input ~ 0
CON_CSI_D0_N
Text GLabel 5330 3455 0    39   Input ~ 0
CON_CSI_D0_P
Text GLabel 5330 3255 0    39   Input ~ 0
GND
Text GLabel 5330 3055 0    39   Input ~ 0
CON_CSI_D1_N
Text GLabel 5330 2855 0    39   Input ~ 0
CON_CSI_D1_P
Text GLabel 5330 2655 0    39   Input ~ 0
GND
Text GLabel 5330 2255 0    39   Input ~ 0
CON_CSI_CLK_P
Text GLabel 5330 2455 0    39   Input ~ 0
CON_CSI_CLK_N
Text GLabel 5330 2055 0    39   Input ~ 0
GND
Text GLabel 5330 1855 0    39   Input ~ 0
CAM0_PWDN
Text GLabel 5330 1655 0    39   Input ~ 0
CAM0_MCLK
Text GLabel 5330 1455 0    39   Input ~ 0
CAM_I2C_SCL
Text GLabel 5330 1255 0    39   Input ~ 0
CAM_I2C_SDA
Text GLabel 5330 1055 0    39   Input ~ 0
VDD_3V3_SLP
Text GLabel 7175 895  0    39   Input ~ 0
DVDD_CAM_IO_1V8
$Comp
L AT24CS02-MAHM U1
U 1 1 5A836D8D
P 8645 1530
F 0 "U1" H 8445 1780 50  0000 C CNN
F 1 "AT24CS02-MAHM" H 8945 1230 50  0000 C CNN
F 2 "Housings_SOIC:SOIC-8_3.9x4.9mm_Pitch1.27mm" H 8645 1530 50  0001 C CIN
F 3 "" H 8645 1530 50  0001 C CNN
	1    8645 1530
	1    0    0    -1  
$EndComp
$Comp
L C C7
U 1 1 5A8372A7
P 10380 1495
F 0 "C7" H 10405 1595 50  0000 L CNN
F 1 "0.1uF" H 10405 1395 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 10418 1345 50  0001 C CNN
F 3 "" H 10380 1495 50  0001 C CNN
	1    10380 1495
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR01
U 1 1 5A8376FB
P 8645 1930
F 0 "#PWR01" H 8645 1680 50  0001 C CNN
F 1 "GND" H 8645 1780 50  0000 C CNN
F 2 "" H 8645 1930 50  0001 C CNN
F 3 "" H 8645 1930 50  0001 C CNN
	1    8645 1930
	1    0    0    -1  
$EndComp
Text GLabel 6670 2425 0    39   Input ~ 0
GND
$Comp
L GND #PWR02
U 1 1 5A837B1C
P 7790 2425
F 0 "#PWR02" H 7790 2175 50  0001 C CNN
F 1 "GND" H 7790 2275 50  0000 C CNN
F 2 "" H 7790 2425 50  0001 C CNN
F 3 "" H 7790 2425 50  0001 C CNN
	1    7790 2425
	1    0    0    -1  
$EndComp
$Comp
L R R1
U 1 1 5A838084
P 7050 1655
F 0 "R1" V 7130 1655 50  0000 C CNN
F 1 "4,7k" V 7050 1655 50  0000 C CNN
F 2 "Resistors_SMD:R_1206" V 6980 1655 50  0001 C CNN
F 3 "" H 7050 1655 50  0001 C CNN
	1    7050 1655
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 5A838127
P 7315 1650
F 0 "R2" V 7395 1650 50  0000 C CNN
F 1 "4,7k" V 7315 1650 50  0000 C CNN
F 2 "Resistors_SMD:R_1206" V 7245 1650 50  0001 C CNN
F 3 "" H 7315 1650 50  0001 C CNN
	1    7315 1650
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR03
U 1 1 5A8382F8
P 7050 1805
F 0 "#PWR03" H 7050 1555 50  0001 C CNN
F 1 "GND" H 7050 1655 50  0000 C CNN
F 2 "" H 7050 1805 50  0001 C CNN
F 3 "" H 7050 1805 50  0001 C CNN
	1    7050 1805
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR04
U 1 1 5A838366
P 7315 1800
F 0 "#PWR04" H 7315 1550 50  0001 C CNN
F 1 "GND" H 7315 1650 50  0000 C CNN
F 2 "" H 7315 1800 50  0001 C CNN
F 3 "" H 7315 1800 50  0001 C CNN
	1    7315 1800
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 5A838422
P 7705 1215
F 0 "R3" V 7785 1215 50  0000 C CNN
F 1 "4,7k" V 7705 1215 50  0000 C CNN
F 2 "Resistors_SMD:R_1206" V 7635 1215 50  0001 C CNN
F 3 "" H 7705 1215 50  0001 C CNN
	1    7705 1215
	0    1    1    0   
$EndComp
Text Notes 10775 2220 2    51   ~ 0
Dirección I2C: 7'h54 -> b1010100\n
Text Notes 10825 920  2    59   ~ 0
EEPROM (CAT2402HU4IGT3A)
Text GLabel 9045 1430 2    59   Input ~ 0
CAM_I2C_SDA
Text GLabel 9045 1580 2    59   Input ~ 0
CAM_I2C_SCL
Text Notes 9915 4610 2    59   ~ 0
Alimentaciones del sistema\n
Text GLabel 5330 1155 0    39   Input ~ 0
VDD_3V3_SLP
Text GLabel 5330 1355 0    39   Input ~ 0
CAM_I2C_SDA
Text GLabel 5330 1555 0    39   Input ~ 0
CAM_I2C_SCL
Text GLabel 5330 1755 0    39   Input ~ 0
CAM0_MCLK
Text GLabel 5330 1955 0    39   Input ~ 0
CAM0_PWDN
Text GLabel 5330 2155 0    39   Input ~ 0
GND
Text GLabel 5330 2355 0    39   Input ~ 0
CON_CSI_CLK_P
Text GLabel 5330 2555 0    39   Input ~ 0
CON_CSI_CLK_N
Text GLabel 5330 2755 0    39   Input ~ 0
GND
Text GLabel 5330 2955 0    39   Input ~ 0
CON_CSI_D1_P
Text GLabel 5330 3155 0    39   Input ~ 0
CON_CSI_D1_N
Text GLabel 5330 3355 0    39   Input ~ 0
GND
Text GLabel 5330 3555 0    39   Input ~ 0
CON_CSI_D0_P
Text GLabel 5330 3755 0    39   Input ~ 0
CON_CSI_D0_N
Text GLabel 5330 3855 0    39   Input ~ 0
GND
Text GLabel 1255 1385 2    39   Input ~ 0
GND
Text GLabel 1255 1585 2    39   Input ~ 0
GND
Text GLabel 1255 1285 2    39   Input ~ 0
VDD_3V3_SLP
Text GLabel 1255 1485 2    39   Input ~ 0
DVDD_CAM_IO_1V8
$Comp
L Conn_01x09 J2
U 1 1 5ADD045C
P 1065 2420
F 0 "J2" H 1065 2920 50  0000 C CNN
F 1 "Conn_01x09" H 1065 1920 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x09_Pitch2.54mm" H 1065 2420 50  0001 C CNN
F 3 "" H 1065 2420 50  0001 C CNN
	1    1065 2420
	-1   0    0    1   
$EndComp
Text GLabel 1265 2020 2    39   Input ~ 0
GND
Text GLabel 1265 2120 2    39   Input ~ 0
CON_CSI_D0_N
Text GLabel 1265 2320 2    39   Input ~ 0
GND
Text GLabel 1265 2220 2    39   Input ~ 0
CON_CSI_D0_P
Text GLabel 1265 2420 2    39   Input ~ 0
CON_CSI_D1_N
Text GLabel 1265 2520 2    39   Input ~ 0
CON_CSI_D1_P
Text GLabel 1265 2620 2    39   Input ~ 0
GND
Text GLabel 1265 2720 2    39   Input ~ 0
CON_CSI_CLK_N
Text GLabel 1265 2820 2    39   Input ~ 0
CON_CSI_CLK_P
$Comp
L Conn_01x03 J3
U 1 1 5ADD2566
P 1075 3370
F 0 "J3" H 1075 3570 50  0000 C CNN
F 1 "Conn_01x03" H 1075 3170 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 1075 3370 50  0001 C CNN
F 3 "" H 1075 3370 50  0001 C CNN
	1    1075 3370
	-1   0    0    1   
$EndComp
Text GLabel 1275 3470 2    39   Input ~ 0
GND
Text GLabel 1275 3370 2    39   Input ~ 0
CAM0_PWDN
Text GLabel 1275 3270 2    39   Input ~ 0
CAM0_MCLK
$Comp
L Conn_01x03 J4
U 1 1 5ADD2FAA
P 1075 3990
F 0 "J4" H 1075 4190 50  0000 C CNN
F 1 "Conn_01x03" H 1075 3790 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x03_Pitch2.54mm" H 1075 3990 50  0001 C CNN
F 3 "" H 1075 3990 50  0001 C CNN
	1    1075 3990
	-1   0    0    1   
$EndComp
Text GLabel 1275 4090 2    39   Input ~ 0
GND
Text GLabel 1275 3990 2    39   Input ~ 0
CAM_I2C_SCL
Text GLabel 1275 3890 2    39   Input ~ 0
CAM_I2C_SDA
$Comp
L Conn_01x06 J1
U 1 1 5ADE08C3
P 1055 1385
F 0 "J1" H 1055 1685 50  0000 C CNN
F 1 "Conn_01x06" H 1055 985 50  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_1x06_Pitch2.54mm" H 1055 1385 50  0001 C CNN
F 3 "" H 1055 1385 50  0001 C CNN
	1    1055 1385
	-1   0    0    1   
$EndComp
Text GLabel 1255 1185 2    39   Input ~ 0
GND
Text GLabel 1255 1085 2    39   Input ~ 0
AVDD_CAM_2V8
$Comp
L C C1
U 1 1 5ADE1954
P 6640 3160
F 0 "C1" H 6665 3260 50  0000 L CNN
F 1 "0,1 uF" H 6665 3060 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 6678 3010 50  0001 C CNN
F 3 "" H 6640 3160 50  0001 C CNN
	1    6640 3160
	1    0    0    -1  
$EndComp
$Comp
L C C3
U 1 1 5ADE1A55
P 6985 3160
F 0 "C3" H 7010 3260 50  0000 L CNN
F 1 "0,1 uF" H 7010 3060 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 7023 3010 50  0001 C CNN
F 3 "" H 6985 3160 50  0001 C CNN
	1    6985 3160
	1    0    0    -1  
$EndComp
$Comp
L C C5
U 1 1 5ADE1AC6
P 7370 3155
F 0 "C5" H 7395 3255 50  0000 L CNN
F 1 "4,7 uF" H 7395 3055 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 7408 3005 50  0001 C CNN
F 3 "" H 7370 3155 50  0001 C CNN
	1    7370 3155
	1    0    0    -1  
$EndComp
$Comp
L C C6
U 1 1 5ADE1B39
P 7775 3150
F 0 "C6" H 7800 3250 50  0000 L CNN
F 1 "0,1 uF" H 7800 3050 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 7813 3000 50  0001 C CNN
F 3 "" H 7775 3150 50  0001 C CNN
	1    7775 3150
	1    0    0    -1  
$EndComp
$Comp
L D_Zener D2
U 1 1 5ADE1BB4
P 8260 3145
F 0 "D2" H 8260 3245 50  0000 C CNN
F 1 "D_Zener" H 8260 3045 50  0000 C CNN
F 2 "Diodes_SMD:D_2010" H 8260 3145 50  0001 C CNN
F 3 "" H 8260 3145 50  0001 C CNN
	1    8260 3145
	0    1    1    0   
$EndComp
$Comp
L GND #PWR05
U 1 1 5ADE1D9D
P 7370 3415
F 0 "#PWR05" H 7370 3165 50  0001 C CNN
F 1 "GND" H 7370 3265 50  0000 C CNN
F 2 "" H 7370 3415 50  0001 C CNN
F 3 "" H 7370 3415 50  0001 C CNN
	1    7370 3415
	1    0    0    -1  
$EndComp
Wire Notes Line
	530  810  4145 810 
Wire Notes Line
	4265 805  4265 4665
Wire Notes Line
	4265 4665 6185 4665
Wire Notes Line
	6185 4665 6185 805 
Wire Notes Line
	6185 805  4265 805 
Wire Wire Line
	8645 1180 10380 1180
Wire Wire Line
	10380 1180 10380 1345
Wire Wire Line
	10380 1930 10380 1645
Wire Wire Line
	8245 1930 10380 1930
Wire Wire Line
	7790 2425 6670 2425
Wire Wire Line
	8245 1730 8245 1930
Connection ~ 8645 1930
Wire Wire Line
	8245 1480 7315 1480
Wire Wire Line
	7315 1480 7315 1500
Wire Wire Line
	8245 1380 7050 1380
Wire Wire Line
	7050 1380 7050 1505
Wire Wire Line
	7175 895  7175 1215
Wire Wire Line
	7175 1215 7555 1215
Wire Wire Line
	7855 1215 7855 1580
Wire Wire Line
	7855 1580 8245 1580
Wire Notes Line
	6425 805  6425 2270
Wire Notes Line
	6425 2270 10880 2270
Wire Notes Line
	10880 2270 10880 800 
Wire Notes Line
	10880 800  6425 800 
Wire Wire Line
	7175 970  8645 970 
Wire Wire Line
	8645 970  8645 1180
Connection ~ 7175 970 
Wire Notes Line
	530  810  530  4675
Wire Notes Line
	530  4675 4145 4675
Wire Notes Line
	4145 4675 4145 810 
Wire Wire Line
	8260 3400 8260 3295
Wire Wire Line
	6640 3400 8260 3400
Wire Wire Line
	7370 3305 7370 3415
Connection ~ 7370 3400
Wire Wire Line
	7775 3300 7775 3400
Connection ~ 7775 3400
Wire Wire Line
	6985 3400 6985 3310
Wire Wire Line
	6640 3400 6640 3310
Connection ~ 6985 3400
Wire Wire Line
	6640 3010 6640 2845
Wire Wire Line
	6640 2845 8260 2845
Wire Wire Line
	8260 2845 8260 2995
Wire Wire Line
	7775 3000 7775 2845
Connection ~ 7775 2845
Wire Wire Line
	6985 3010 6985 2845
Connection ~ 6985 2845
Wire Wire Line
	7370 2640 7370 3005
Connection ~ 7370 2845
Text GLabel 7310 2640 0    39   Input ~ 0
DVDD_CAM_IO_1V8
Wire Wire Line
	7370 2640 7310 2640
$Comp
L C C2
U 1 1 5ADE35AC
P 6660 4040
F 0 "C2" H 6685 4140 50  0000 L CNN
F 1 "4,7 uF" H 6685 3940 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 6698 3890 50  0001 C CNN
F 3 "" H 6660 4040 50  0001 C CNN
	1    6660 4040
	1    0    0    -1  
$EndComp
$Comp
L C C4
U 1 1 5ADE3675
P 7215 4040
F 0 "C4" H 7240 4140 50  0000 L CNN
F 1 "0,1 uF" H 7240 3940 50  0000 L CNN
F 2 "Capacitors_SMD:C_1206_HandSoldering" H 7253 3890 50  0001 C CNN
F 3 "" H 7215 4040 50  0001 C CNN
	1    7215 4040
	1    0    0    -1  
$EndComp
$Comp
L D_Zener D1
U 1 1 5ADE3783
P 7730 4025
F 0 "D1" H 7730 4125 50  0000 C CNN
F 1 "D_Zener" H 7730 3925 50  0000 C CNN
F 2 "Diodes_SMD:D_2010" H 7730 4025 50  0001 C CNN
F 3 "" H 7730 4025 50  0001 C CNN
	1    7730 4025
	0    1    1    0   
$EndComp
$Comp
L GND #PWR06
U 1 1 5ADE385E
P 7215 4355
F 0 "#PWR06" H 7215 4105 50  0001 C CNN
F 1 "GND" H 7215 4205 50  0000 C CNN
F 2 "" H 7215 4355 50  0001 C CNN
F 3 "" H 7215 4355 50  0001 C CNN
	1    7215 4355
	1    0    0    -1  
$EndComp
Wire Wire Line
	6660 3890 6660 3775
Wire Wire Line
	6660 3775 7730 3775
Wire Wire Line
	7730 3775 7730 3875
Wire Wire Line
	7215 3585 7215 3890
Connection ~ 7215 3775
Wire Wire Line
	6660 4190 6660 4265
Wire Wire Line
	6660 4265 7730 4265
Wire Wire Line
	7730 4265 7730 4175
Wire Wire Line
	7215 4190 7215 4355
Connection ~ 7215 4265
Text GLabel 7150 3585 0    39   Input ~ 0
AVDD_CAM_2V8
Wire Wire Line
	7215 3585 7150 3585
Wire Notes Line
	6290 2370 6290 4650
Wire Notes Line
	6290 4650 10015 4650
Wire Notes Line
	10015 4650 10015 2350
Wire Notes Line
	10015 2350 6290 2350
Wire Notes Line
	6290 2350 6290 2375
$EndSCHEMATC
