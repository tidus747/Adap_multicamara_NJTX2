# Conexión de la cámara de Raspberry Pi (Sensor IMX219, V2.1) con Nvidia Jetson TX2

## Introducción

En esta guía explicaremos todos los pasos seguidos para la correcta generación de los ficheros necesarios en la conexión del **sensor IMX219**. Para este propósito en primer lugar, definiremos los pasos a seguir en el desarrollo para la implementación de los módulos de cámra. Todos los recursos que hemos utilizado para el desarrollo de esta guía, se encuentran al final de la misma.

## Preparación de elementos necesarios (Hardware/Software)

Antes de comenzar con el desarrollo es necesario contar con una serie de elementos básicos tanto de software como de hardware. Comenzaremos con los elementos de hardware necesarios y continuaremos enumerando los elementos de software.

### Hardware

Lo primero que necesitaremos será el kit de desarrollo de [Nvidia Jetson TX2](https://www.nvidia.es/autonomous-machines/embedded-systems-dev-kits-modules/). Por otro lado, necesitaremos un dispositivo que nos permita conectar las cámaras a la Jetson TX2, en nuestro caso hemos optado por el conector [J20 de Auvidea](https://auvidea.com/j20/). Por último, necesitaremos los módulos de cámara que implementaremos en nuestra placa. En este caso tenemos dos opciones si hablamos de módulos compatibles con Raspberry Pi. Podemos optar por la [versión 2.1](https://www.raspberrypi.org/products/camera-module-v2/) o por la [versión 1.3](https://uk.pi-supply.com/products/raspberry-pi-camera-board-v1-3-5mp-1080p). Optaremos por implementar la versión más actualizada de este sensor, esta es la versión 2.1.

- Sensor OV5647 (Versión 1.3 de cámara Rpi)

<p align="center">
  <img width="150" src="https://www.dexterindustries.com/wp-content/uploads/2015/07/Raspberry-Pi-Camera.jpg">
</p>
     
- Sensor IMX219 (Version 2.1 de cámara Rpi)

<p align="center">
  <img width="150" src="http://img.dxcdn.com/productimages/sku_433744_1.jpg">
</p>

### Software

Con respecto al software necesario para la implementación de esta herramienta, necesitaremos lo siguiente:

- [Ubuntu 16.04 LTS](http://releases.ubuntu.com/16.04/), para la programación y la carga del nuevo kernel en la NVDIA Jetson (tanto para la TX1 como para la TX2) es necesario contar con este sistema operativo. Esto es así debido a que el SDK desarrollado por NVIDIA para la carga del código está especificamente desarrollado para este sistema.
- [SDK Jetson TX1/TX2](https://developer.nvidia.com/embedded/jetpack), el NVIDIA Jetpack nos proporciona las herramientas necesarias para la descarga y la modificación del código fuente de las NVIDIA Jetson. Por otro lado, también instalará en nuestro sistema herramientas como TensorFlow o ejemplos para la renderización con CUDA que posteriormente podrías ser implementados en el kit de desarrollo.
- [Linaro ToolChain](http://releases.linaro.org/components/toolchain/binaries/5.3-2016.02/), esta herramienta nos servirá para compilar el kernel de la NVIDIA Jetson en nuestro sistema y posteriormente cargarlo en la placa.

## Implementación del sensor a nivel de Software

Antes de comenzar, debemos determinar cuales son los pasos que debemos ejecutar para la correcta implementación del código en la plataforma:

1. Preparar los ficheros fuente del *Device Tree*
2. Modificar los archivos del *Device Tree* correctamente.
3. Modificar los ficheros fuente del módulo de cámara. 
4. Configurar el Kernel para detectar los módulos qe hemos añadido.
5. Compilar el kernel.
6. Cargar el kernel en la NVIDIA Jetson TX2.
7. Cargar los **DTB** en la Jetson TX2.
8. Testear el correcto funcionamiento del sistema.

Una vez hemos definido los pasos a seguir, podemos introducir cada uno de ellos con un mayor nivel de detalle.

### Preparación de ficheros fuente del *Device Tree* 

En general, en los sistemas Linux, existen dos formas de modificar el kernel. Los dos métodos son los siguientes:

- Mediante el **Archivo de configuración del kernel**: esto le indicará al kernel qué características y controladores deberían compilarse. También puede especificar qué controladores deben empaquetarse en el kernel y cuáles deben compilarse pero separarse del kernel. En nuestro caso, modificaremos esto para decirle al kernel que cree compatibilidad con el controlador IMX219.

- Mediante el **Device Tree Source (DTS)**: así es como puede configurar el núcleo en el arranque para que se comporte de manera diferente en una placa frente a otra. Un claro ejemplo lo podmeos encontrar con la Raspberry Pi y la Raspberry Pi Zero. Estas dos placas son muy diferentes a simple vista pero tienen el mismo kernel porque hay dos archivos DTS diferentes para él.

Como hemos comentado, necesitamos agregar soporte para la cámara IMX219 (Cámara Raspberry Pi Modelo 2.1). Debido a que no existe un mecanismo para reconocer las cámaras CSI mientras el kernel se está ejecutando, tenemos que modificar el **DTS** para decirle al kernel cómo reconocerlas. Esto es muy diferente con respecto al funcionamiento de un USB, por ejemplo, porque en el caso del USB existe un mecanismo estándar que el kernel puede usar para reconocer cuando se inserta un nuevo dispositivo, para el CSI esto no es así. Por lo tanto, cada placa está configurada con un archivo interno conocido como **DTB (Device Tree Binary)**. Este **DTB** es una versión compilada de los archivos **DTS (Device Tree Source)** y **DTSi (Device Tree Source Include)**.

Necesitamos configurar el archivo DTS para reconocer la cámara IMX219, para hacer esto tenemos que describir lo siguiente:

- A qué puertos CSI están conectadas las cámaras.
- Cómo se deben configurar las cámaras usando I2C.
- Qué modos de visualización tienen las cámaras (¿Tiene 1920x1080 y / o 1280x720).
- Cómo configurar la arquitectura de entrada de video del TX2.

Todo esto debe recogerse en un fichero **DTS**. Podemos este fichero desde cero, pero para la gran mayoría de casos puede usarse el archivo **DTS** predeterminado utilizado para los kits de desarollo de NVIDIA. En el caso de que se quiera obtener un mayor control sobre este procedimiento puede consultarse el siguiente [enlace](https://cospandesign.github.io/linux/2017/10/27/tx2-bringup.html). En nuestro caso, optaremos por crear nuestro fichero **DTS** partiendo de los códigos creados por NVIDIA. La ruta predefinida para localizar el fichero de configuración predeterminado en la Jetson TX2 es:

```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/quill/kernel-dts/tegra186-quill-p3310-1000-c03-00-base.dts
```
En la ruta anterior podemos encontrar algo de información aunque realmente, gran parte de la configuración se encuentra en esta otra ruta:

```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/quill/kernel-dts/tegra186-quill-p3310-1000-a00-00-base.dts
```

Antes de continuar, es probable que aún no dispongas de los ficheros que hemos mencionado por lo que será necesario descargarlos. En la siguiente sección explicaremos como realizar este proceso correctamente.

### Descarga del NVIDIA JetPack 3.2 y los ficheros fuente del kernel

#### Descarga del NVIDIA JetPack

1. Descarga la versión 3.2 (o su versión más reciente) desde el siguiente [enlace](https://developer.nvidia.com/embedded/dlc/jetpack-l4t-3_2-ga).
2. Mueve los archivos binarios que acabas de descargar a un directorio donde quieras que ocurra la instalación. La ruta recomendada sería `/home/$USER/JetPack-L4T-3.2`. En tal caso, los comandos a introducir en el terminal serían los siguientes:

```
mkdir -p /home/$USER/JetPack-L4T-3.2
mv JetPack-L4T-3.2-linux-x64_b196.run /home/$USER/JetPack-L4T-3.2/
```

3. Marcamos como ejecutable el archivos y le asignamos los permisos.

```
cd /home/$USER/JetPack-L4T-3.2
chmod +x JetPack-L4T-3.2-linux-x64_b196.run
```

4. Instalar el JetPack.

```
./JetPack-L4T-3.2-linux-x64_b196.run
```

5. Sigue las instrucciones para la instalación. Selecciona la placa en el instalador (TX1, TX2, TX2i).

#### Descarga de los ficheros fuente del kernel

Para descargar todos los ficheros necesarios llamaremos `$DEVDIR` al directorio donde se encuentran los ficheros de desarrollo. En el caso de haber usado los comandos indtroducidos anteriormente tendríamos: 

- **Para la TX1**
```
export DEVDIR=$HOME/JetPack-L4T-3.2/64_TX1/Linux_for_Tegra
```
- **Para la TX2**
```
export DEVDIR=$HOME/JetPack-L4T-3.2/64_TX2/Linux_for_Tegra
```

Para descargar todos los ficheros fuente, usaremos el script *source_sync.sh* 

```
cd $DEVDIR/
./source_sync.sh
```

Este comando descargará además el bootloader y el kernel. Cuando el script pregunte por el tag que queremos sincronizar, introducir **tegra-l4t-r28.2** en ambos casos.

### Modificación de ficheros fuente del *Device Tree* 

Una vez hemos descargado los ficheros fuente, modificaremos el fichero disponible en la siguiente ruta:

```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/quill/kernel-dts/tegra186-quill-p3310-1000-a00-00-base.dts
```

Para simplificar el desarrollo, se desactivará el soporte inteligente para la administración de cámaras de NVIDIA y se eliminarán las referencias a otros módulos de cámara. El fichero tendría el siguiente aspecto:

```
#include <t18x-common-platforms/tegra186-quill-common-p3310-1000-a00.dtsi>
#include <t18x-common-platforms/tegra186-quill-power-tree-p3310-1000-a00-00.dtsi>
//#include <t18x-common-platforms/tegra186-quill-camera-modules.dtsi>
#include <t18x-common-modules/tegra186-display-e3320-1000-a00.dtsi>

/* comms dtsi file should be included after gpio dtsi file */
#include <t18x-common-platforms/tegra186-quill-comms.dtsi>
#include <t18x-common-plugin-manager/tegra186-quill-p3310-1000-a00-plugin-manager.dtsi>
#include <t18x-common-modules/tegra186-super-module-e2614-p2597-1000-a00.dtsi>
#include <t18x-common-plugin-manager/tegra186-quill-display-plugin-manager.dtsi>
#include <t18x-common-prod/tegra186-priv-quill-p3310-1000-a00-prod.dtsi>
//#include <t18x-common-plugin-manager/tegra186-quill-camera-plugin-manager.dtsi>

#include <dt-bindings/linux/driver-info.h>
```

Ahora que hemos eliminado todas las referencias a las cámaras anteriores, vamos a agregar dos archivos. Uno que configurará la(s) cámara(s) de nivel de la placa y el otro para configurar la arquitectura interna de la Interfaz de video de la Jetson TX2.

Para ello, crearemos un nuevo archivo llamado *tegra186-my-camera-config-a00.dtsi* en el siguiente directorio:
```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-platforms/
```
Crearemos un segundo fichero con el mismo nombre en este otro directorio:
```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-modules/
```

El fichero *my-camera-config* se puede cambiar a lo que quieras y *a00* es solo la primera versión de este archivo.

Por el momento, usaremos la versión alojada en *platforms* del archivo como paso para el módulo, pero técnicamente se pueden anular los *modules* abstractos previstos para alguna plataforma general.

Dentro de la versión de *platforms* del archivo, incluimos la siguiente línea:
```
#include <t18x-common-modules/tegra186-my-camera-config-a00.dtsi>

```
Dentro del fichero de configuración necesitamos configurar una serie de parámetros para que la cámara sea capaz de funcionar. Los módulos son los siguientes:

* Permitir que los GPIOs de la Jetson TX2 puedan tener las siguientes funcionalidades:
    * Resetear las líneas
    * Posible incorporación de un multiplexor de direcciones I2C
* TX2’s host1x
    * Componente NVCSI: Este componente servirá para configurar las líneas CSI para comunicarse con las cámaras correctamente.
    * Componente VI: Configura la salida del NVCSI de forma directa a las líneas del ISP o directamente sobre la memoria del dispositivo.
    * Componente I2C: Configuración de la salida de la cámara a vídeo.
* GPIOs
    * Configurar los GPIOs para que posean cierto comportamiento como por ejemplo, resetear la cámara, encenderla o apagar sus reguladores.
* *Tegra-camera-platform*
    * Describir la localización física de la cámara.
    * Configurar el ISP para procesar las imágenes.
    * Describir otros elementos que puedan hacer falta a la cámara, como por ejemplo el enfoque.

Para comprender mejor todo lo anterior, se ha ilustrado la idea principal en la siguiente imagen:

<p align="center">
  <img width="800" src="http://cospandesign.github.io/assets/image/posts/rpi-camera/rpi_video_subsystem.png">
</p>

Todas las cámaras de Raspberry Pi tienen la misma dirección I2C, por lo que necesitamos una manera de distinguir una cámara de otra. La manera más fácil es con un multiplexor. Por esta razón, usaremos un multiplexor GPIO ya que el controlador para esta ya está integrado en el kernel.

En alto nivel si observamos la figura anterior, los datos de las cámaras de  Raspberry Pi llegan a la Jetson TX2 a través de los canales CSI representados en azul. Solo necesitamos un bus CSI de dos canales en este caso así que tomamos CSI A, si necesitáramos cuatro canales, reservaríamos dos bloques. El núcleo **NVCSI** extraerá la imagen sin formato del protocolo CSI y enviará los datos a **VI**. Este componente *Video Input* es esencialmente un enrutador de video, enruta el video al ISP o directamente a la memoria del dispositivo. Si la cámara de Raspberry Pi tiene un procesador de señal de imagen interno para convertir la imagen a una imagen RGB útil, le diremos al VI que enrute los datos de imagen a la memoria, pero como la cámara no tiene un ISP, usamos el ISP que posee la Jetson TX2. El proceso de enrutar los datos de video después del componente **VI** se realiza dentro del territorio del usuario cuando el kernel se inicia, por lo que terminamos una vez que el **VI** está conectado correctamente y el usuario ya tiene acceso a los datos.

Una vez comprendido todo esto, descargaremos los siguientes ficheros:

- [module tegra186-my-config-a00.dtsi](http://cospandesign.github.io/assets/files/posts/rpi-camera/tegra186-my-config-camera-a00_MODULE.dtsi)
- [platform tegra186-my-config-a00.dtsi](http://cospandesign.github.io/assets/files/posts/rpi-camera/tegra186-my-config-camera-a00_PLATFORM.dtsi)

Los directorios para guardar estos ficheros serían los siguientes:

```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-modules/
```
```
Linux_for_Tegra/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-platforms/
```
Por último, es necesario incluir el fichero `tegra186-my-camera-config-a00.dtsi` en la cabecera de nuestro fichero **dts** de configuración base del sistema. En el interior del fichero `tegra186-quill-p3310-1000-c03-00-base.dts` debemos añadir la siguiente línea:

```
#include <t18x-common-platforms/tegra186-my-camera-config-a00.dtsi>
```

Debería tener el siguiente aspecto:

```
#include "tegra186-quill-p3310-1000-a00-00-base.dts"
#include <t18x-common-platforms/tegra186-my-camera-config-a00.dtsi>

/ {
  nvidia,dtsfilename = __FILE__;
  nvidia,dtbbuildtime = __DATE__, __TIME__;
  ...
```

Una vez hecho esto podemos pasar a realizar las modificaciones sobre los módulos de cámara.

### Modificación de ficheros fuente del módulo de cámara

Lamentablemente, el controlador para el sensor **IMX219** suministrado por NVIDIA no es compatible con el módulo de Raspberry Pi. Por lo tanto, es necesario realizar algunas pequeñas modificaciones. Entre otras cosas, los requisitos del regulador deben eliminarse y las tablas de modos deben modificarse. Para realizar dicha modificación simplemente descargue los siguientes archivos:

- [imx219.c](http://cospandesign.github.io/assets/files/posts/rpi-camera/imx219.c)
- [imx219_mode_tbls.h](http://cospandesign.github.io/assets/files/posts/rpi-camera/imx219_mode_tbls.h)

Sobrescribe los ficheros existentes en el siguiente directorio con los descargados anteriormente:

```
Linux_for_Tegra/sources/kernel/kernel-4.4/drivers/media/i2c
```

### Configuración del kernel para detectar los módulos añadidos

Una vez descargado e instalado [toolchain](http://developer.ridgerun.com/wiki/index.php?title=Compiling_Tegra_X1/X2_source_code#Toolchain) podremos preparar el Kernel para su compilación. Durante la preparación, configuraremos los archivos que queremos compilar y entre ellos añadiremos los ficheros que hemos modificado y los módulos que necesitamos para el correcto funcionamiento de las cámaras.

EL primer paso será configurar el entorno que vamos a utilizar, introduciendo los comandos siguientes:

```
mkdir -p $DEVDIR/images/modules 
mkdir -p $DEVDIR/images/packages 
export CROSS_COMPILE=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
export CROSS32CC=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc
export KERNEL_MODULES_OUT=$DEVDIR/images/modules
export TEGRA_KERNEL_OUT=$DEVDIR/images
export ARCH=arm64
```

Limpiamos la configuración anterior del kernel:

```
cd $DEVDIR/sources/kernel/kernel-4.4
make mrproper
```

Configuramos el kernel:

```
make O=$TEGRA_KERNEL_OUT tegra18_defconfig
make O=$TEGRA_KERNEL_OUT menuconfig
```

**IMPORTANTE**: Para ejecutar el paso anterior, es posible que necesites instalar los siguientes paquetes si obtienes algún error al ejecutarlo.

```
sudo apt-get install libncurses5 libncurses5-dev
```

Al ejecutar el comando `make O=$TEGRA_KERNEL_OUT menuconfig` nos aparecerá un menú en el que podremos configurar los módulos que queremos cargar para su compilación en el kernel. La ventana que nos aparecerá en nuestro terminal será igual a la que vemos en la siguiente imagen:

<p align="center">
  <img width="600" src="http://cospandesign.github.io/assets/image/posts/rpi-camera/kernel-menu-config.png">
</p>

Dentro de este menú debemos buscar un módulo llamado *i2c-gpio-mux*. Para ello pulsaremos `/` para abrir el buscador y posteriormente escribiremos `I2C_MUX_GPIO`, pulsamos **enter** y debería aparecer lo siguiente:

<p align="center">
  <img width="600" src="http://cospandesign.github.io/assets/image/posts/rpi-camera/kernel-menu-config-i2c-mux-gpio.png">
</p>

Presiona la tecla *1* hasta que aparezca un nuevo menú y posteriormente la tecla *y* para que un * aparezca en la selección de la siguiente manera:

<p align="center">
  <img width="600" src="http://cospandesign.github.io/assets/image/posts/rpi-camera/select-i2c-mux-gpio.png">
</p>

Haremos lo mismo para buscar el módulo de cámara IMX219. Una vez hecho esto, usaremos las flechas de dirección para guardar la configuración. El archivo debe tener el nombre por defecto, es decir, `.config`. Configurado el Kernel podemos pasar a su compilación.

### Compilación del kernel y los DTB

Una vez realizados los pasos anteriores ya podemos compilar el kernel de nuestro sistema.

```
make O=$TEGRA_KERNEL_OUT zImage
make O=$TEGRA_KERNEL_OUT dtbs
make O=$TEGRA_KERNEL_OUT modules
make O=$TEGRA_KERNEL_OUT modules_install INSTALL_MOD_PATH=$KERNEL_MODULES_OUT
```
Después de esto la imagen del kernel que hemos compilado se encontraría en la siguiente ruta:

```
$DEVDIR/images/arch/arm64/boot/Image
```

Y el *devicetree* se encontraría en:
```
$DEVDIR/images/arch/arm64/boot/dts/*.dtb
```

El siguiente paso sería crear un archivo que llamaremos *kernel_supplements.tbz2* y que contendrá los módulos del kernel que hemos compilado. Este archivo es uno de los requerimientos que tiene **Jetpack**.

```
cd $DEVDIR/images/modules/lib/modules/
ls .
```
Definiremos una variable con el mismo nombre que nos aparece al introducir el comando anterior:

```
export KERNEL_MODULES_NAME=4.4.38+
```
Reparamos los links simbólicos que se encuentran en el directorio de los módulos del kernel:

```
cd $DEVDIR/images/modules/lib/modules/$KERNEL_MODULES_NAME
rm build source
```

Creamos un *tarball*:

```
cd $DEVDIR/images/modules/
tar -cjf kernel_supplements.tbz2 *
mv kernel_supplements.tbz2 $DEVDIR/images/packages
```
Además de crear los módulos y la imagen del kernel, necesitamos volver a crear su archivo *kernel_headers.tbz2* (necesario para Jetpack). Por defecto, cuando se aplica algún parche al código del kernel y no se verifican sus cambios en el kernel, se agregará un sufijo -dirty a la versión de lanzamiento (compruebe `ls $DEVDIR/images/modules/lib/modules/` por ejemplo). Por esta razón específica necesitamos generar sus encabezados *tarball* de nuevo cambiando la versión de lanzamiento.

```
cd $DEVDIR/kernel
tar -xf kernel_headers.tbz2
```
Buscamos el nombre de la carpeta que contiene los *headers*, en nuestro caso es *linux-headers-4.4.38-tegra*:

```
ls | grep linux-headers
linux-headers-4.4.38-tegra
export KERNEL_HEADERS_NAME=linux-headers-4.4.38-tegra
```

Renombramos la carpeta:

```
mv $KERNEL_HEADERS_NAME linux-headers-$KERNEL_MODULES_NAME
tar -cjf kernel_headers_custom.tbz2 linux-headers-$KERNEL_MODULES_NAME
mv kernel_headers_custom.tbz2 $DEVDIR/images/packages
rm -rf linux-headers-$KERNEL_MODULES_NAME 
```

Creamos una copia de segurar de la imagen y los paquetes incluidos en el JetPack:

```
mkdir -p $DEVDIR/images/packages-backup
cp -rf $DEVDIR/kernel/* $DEVDIR/images/packages-backup
```

Copiamos el fichero DTB:
```
cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb
```
El paso final consiste en sobreescribir las imágenes por defecto con la imagen que hemos generado durante la compilación para instalarlas usando JetPack.

```
cd $DEVDIR/images
cp -rf arch/arm64/boot/Image arch/arm64/boot/zImage packages/kernel_supplements.tbz2 $DEVDIR/kernel/
cp -rf packages/kernel_headers_custom.tbz2 $DEVDIR/kernel/kernel_headers.tbz2
```

Ejecutamos el script *apply_binaries.sh* para generar la imagen que se va a cargar en la Jetson TX2.

```
cd $DEVDIR/
sudo ./apply_binaries.sh
```
### Carga del Kernel en la Nvidia Jetson TX2

1. Realizamos una copia de seguridad de nuestra imagen del sistema

```
cd $DEVDIR/bootloader/
mv system.img.raw system.img $DEVDIR/images/packages-backup/
```

2. Ejecutamos el Jetpack al igual que la primera vez que lo instalamos en nuestro sistema:

```
cd $DEVDIR/../../
JetPack-L4T-3.2-linux-x64_b196.run
```

JetPack se dará cuenta de que todo ya está construido e instalará sus nuevas imágenes en la Jetson TX2. Si tiene problemas para detectar la dirección IP espere unos 2 minutos y le dará la opción de ingresarla manualmente.

### Cargar los DTB en la Jetson TX2

En versiones anteriores de JetPack, actualizar el DTB era tan fácil como reemplazar el de la carpeta de arranque del directorio de inicio y también podía cambiar la entrada del FDT en `/boot/extlinux/extlinux.conf` para usar una diferente. Para **Jetpack 3.1** esto se modificó y se utiliza una partición separada para actualizar el archivo **DTB** y Nvidia dice que solo se puede actualizar mostrándolo de nuevo usando el script flash provisto.

```
$DEVDIR/images/arch/arm64/boot/dts/*.dtb
```
Remplazamos el DTB en `$DEVDIR/kernel/dtb``con el que hemos generado. Es recomendable hacer una copia de seguridad del DTB original.

```
cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb
```

Ponemos la placa en modo *recovery_USB* y cargamos la imagen:

```
cd $DEVDIR
sudo ./flash.sh -r -k kernel-dtb jetson-tx2 mmcblk1p1
```
**IMPORTANTE**: Usa mmcblk1p1 para una SDcard y mmcblk0p1 para emmc.

Existe otra forma de hacerlo directamente desde la placa, pero este método suele causar errores:
```
sudo dd if=tegra186-quill-p3310-1000-c03-00-base.dtb of=/dev/mmcblk0p13
```

### Test de funcionamiento

Después de que todo está construido y cargado en la Jetson. Deberían aparecer tener tres nuevas entradas `/dev/videoX`.

El siguiente comando puede utilizarse para capturar un video corto:

```
gst-launch-1.0 -v nvcamerasrc sensor-id=0 fpsRange="30 30" num-buffers=100 ! 'video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)I420, framerate=(fraction)30/1' ! omxh264enc ! 'video/x-h264, width=(int)1920, height=(int)1080, format=(string)I420, framerate=(fraction)30/1' ! h264parse ! qtmux ! filesink location=test.mp4 -e
```

Como se está ejecutando a 30 FPS y captura 100 cuadros, el clip durará 2,33 segundos. Puede jugar con estos valores para modificarlo. También puede cambiar entre diferentes sensores con el valor **id del sensor**.

**NOTA**: Es posible que deba actualizar la memoria caché de configuración de imagen de su ISP para pedirle al kernel que reconstruya la configuración de ISP para su cámara específica. El caché está ubicado en:
```
/var/nvidia/nvcam/configuraciones
```
Borre todos estos archivos y reinicie el TX2 y deberían reconstruirse. Este valor depende de la configuración *tegra-camera-platform*.
## Recursos

A continuación vamos a listar los recursos que se han consultado para el desarrollo de esta guía en la que se pretende ilustrar todo el procedimiento seguido para la modificación del kernel, su compilación y su posterior implementación en la NVIDIA Jetson.

- [Raspberry Pi camera on TX2](http://cospandesign.github.io/linux,tx2,kernel,driver/2017/12/15/tx2-rpi-camera-port.html) - Guía para la conexión de tres módulos de Raspberry.
- [Desarrollo de un módulo de Kernel](http://cospandesign.github.io/linux,kernel,driver/2016/04/15/kernel-driver.html) - Guía básica para el desarrollo de un módulo de Kernel.
- [Porting NVIDIA TX2 to a new platform](https://cospandesign.github.io/linux/2017/10/27/tx2-bringup.html) - Portabilidad de código entre la Jetson TX2 y otras plataformas.
- [Guía de usuario para el desarrollo](https://developer.nvidia.com/embedded/dlc/l4t-documentation-28-1) - Guía para el desarrollo de código para la plataforma Jetson TX2.
- [Tópicos en el Foro de Nvidia](https://devtalk.nvidia.com/default/topic/1009359/jetson-tx2/jetson-tx1-sensor-driver-porting-to-tx2-4-4-kernel-/) - Hilo del foro de desarrolladores de NVIDIA donde se trata el desarrollo de módulos de cámara. 
- [Código fuente TX1](https://github.com/CospanDesign/nvidia-tx1-kernel) - Código fuente de la NVIDIA Jetson TX1.
- [Wiki sobre la compilación de Kernel TX1](http://developer.ridgerun.com/wiki/index.php?title=Compiling_Tegra_X1/X2_source_code#Build_Kernel) Guía para la compilación del kernel de la NVIDIA Jetson TX1.
- [Documentación sobre compilación de Kernel Linux](https://www.kernel.org/doc/Documentation/kbuild/modules.txt) - Web con documentación sobre la compilación del Kernel de Linux.
- [Wiki sobre la compilación de Kernel TX2](http://developer.ridgerun.com/wiki/index.php?title=Compiling_Tegra_X2_source_code) Guía para la compilación del kernel de la NVIDIA Jetson TX2.
- [Aplicación de parches en Kernel](https://www.kernel.org/doc/html/v4.11/process/applying-patches.html) Guía para la aplicación de parches en el Kernel de Linux.
- [Añadir sensor IMX219 a TX1](https://developer.ridgerun.com/wiki/index.php?title=Sony_IMX219_Linux_driver_for_Tegra_X1) Guía para añadir y compilar el código fuente del sensor OV5647 en la NVIDIA Jetson TX1.
- [Guía conector J20](http://developer.ridgerun.com/wiki/index.php?title=Getting_started_guide_for_Auvidea_J20_board) Wiki sobre el conector J20 desarrollado por Auvidea para la utilización de diferentes cámaras en la NVIDIA Jetson TX1/TX2.
