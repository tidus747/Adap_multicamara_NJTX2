#!/bin/bash

# Comenzamos la compilación del sistema
export DEVDIR=$HOME/JetPack-L4T-3.2/64_TX2/Linux_for_Tegra

cd $DEVDIR/
./source_sync.sh -k tegra-l4t-r28.1 -u tegra-l4t-r28.1

# Movemos los archivos que necesitamos modificar en nuestro directorio
cp $HOME/tfm_ivan/Código/Patches_IMX219/IMX219_Modify/imx219.c $DEVDIR/sources/kernel/kernel-4.4/drivers/media/i2c/
cp $HOME/tfm_ivan/Código/Patches_IMX219/IMX219_Modify/imx219_mode_tbls.h $DEVDIR/sources/kernel/kernel-4.4/drivers/media/i2c/

cp $HOME/tfm_ivan/Código/Patches_IMX219/DTSI/Module/tegra186-my-config-camera-a00.dtsi $DEVDIR/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-modules/tegra186-my-camera-config-a00.dtsi
cp $HOME/tfm_ivan/Código/Patches_IMX219/DTSI/Platform/tegra186-my-config-camera-a00.dtsi $DEVDIR/sources/hardware/nvidia/platform/t18x/common/kernel-dts/t18x-common-platforms/tegra186-my-camera-config-a00.dtsi

kate $DEVDIR/sources/hardware/nvidia/platform/t18x/quill/kernel-dts/tegra186-quill-p3310-1000-a00-00-base.dts
kate $DEVDIR/sources/hardware/nvidia/platform/t18x/quill/kernel-dts/tegra186-quill-p3310-1000-c03-00-base.dts

echo -n "Archivos copiados y modificados. Pulsa [ENTER] para continuar...: "
read var_name

mkdir -p $DEVDIR/images/modules 
mkdir -p $DEVDIR/images/packages 
export CROSS_COMPILE=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
export CROSS32CC=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc
export KERNEL_MODULES_OUT=$DEVDIR/images/modules
export TEGRA_KERNEL_OUT=$DEVDIR/images
export ARCH=arm64


cd $DEVDIR/sources/kernel/kernel-4.4
make mrproper

make O=$TEGRA_KERNEL_OUT tegra18_defconfig
make O=$TEGRA_KERNEL_OUT menuconfig

make O=$TEGRA_KERNEL_OUT zImage
make O=$TEGRA_KERNEL_OUT dtbs
make O=$TEGRA_KERNEL_OUT modules
make O=$TEGRA_KERNEL_OUT modules_install INSTALL_MOD_PATH=$KERNEL_MODULES_OUT

# Creamos las copias de los archivos allá donde son necesarios

export KERNEL_MODULES_NAME=4.4.38+
cd $DEVDIR/images/modules/lib/modules/$KERNEL_MODULES_NAME
rm build source
cd $DEVDIR/images/modules/
tar -cjf kernel_supplements.tbz2 *
mv kernel_supplements.tbz2 $DEVDIR/images/packages
cd $DEVDIR/kernel
tar -xf kernel_headers.tbz2

export KERNEL_HEADERS_NAME=linux-headers-4.4.38-tegra
mv $KERNEL_HEADERS_NAME linux-headers-$KERNEL_MODULES_NAME
tar -cjf kernel_headers_custom.tbz2 linux-headers-$KERNEL_MODULES_NAME
mv kernel_headers_custom.tbz2 $DEVDIR/images/packages
rm -rf linux-headers-$KERNEL_MODULES_NAME

mkdir -p $DEVDIR/images/packages-backup
cp -rf $DEVDIR/kernel/* $DEVDIR/images/packages-backup

cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb

cd $DEVDIR/images
cp -rf arch/arm64/boot/Image arch/arm64/boot/zImage packages/kernel_supplements.tbz2 $DEVDIR/kernel/
cp -rf packages/kernel_headers_custom.tbz2 $DEVDIR/kernel/kernel_headers.tbz2

cd $DEVDIR/
sudo ./apply_binaries.sh 

cd $DEVDIR/bootloader/
mv system.img.raw system.img $DEVDIR/images/packages-backup/

echo -n "Ponga la Jetson en modo depuración y pulse [ENTER] para continuar...: "
read var_name

cd $DEVDIR
sudo ./flash.sh -t jetson-tx2 mmcblk0p1

