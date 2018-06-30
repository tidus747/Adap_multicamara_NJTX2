#!/bin/bash

# Script para lanzar la compilación de la NVIDIA Jetson TX2
export DEVDIR=$HOME/JetPack-L4T-3.2/64_TX2/Linux_for_Tegra

export CROSS_COMPILE=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
export CROSS32CC=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc
export KERNEL_MODULES_OUT=$DEVDIR/images/modules
export TEGRA_KERNEL_OUT=$DEVDIR/images
export ARCH=arm64

cd $DEVDIR/sources/kernel/kernel-4.4
make mrproper

make -j 8 O=$TEGRA_KERNEL_OUT tegra18_defconfig
make -j 8 O=$TEGRA_KERNEL_OUT menuconfig

make -j 8 O=$TEGRA_KERNEL_OUT zImage
make -j 8 O=$TEGRA_KERNEL_OUT dtbs
make -j 8 O=$TEGRA_KERNEL_OUT modules
make -j 8 O=$TEGRA_KERNEL_OUT modules_install INSTALL_MOD_PATH=$KERNEL_MODULES_OUT


export KERNEL_MODULES_NAME=4.4.38+

cd $DEVDIR/images/modules/lib/modules/$KERNEL_MODULES_NAME
rm build source

cd $DEVDIR/images/modules/
tar -cjf kernel_supplements.tbz2 *
mv kernel_supplements.tbz2 $DEVDIR/images/packages

cd $DEVDIR/kernel
tar -xf kernel_headers.tbz2

export KERNEL_HEADERS_NAME=linux-headers-4.4.38+
mv $KERNEL_HEADERS_NAME linux-headers-$KERNEL_MODULES_NAME
tar -cjf kernel_headers_custom.tbz2 linux-headers-$KERNEL_MODULES_NAME
mv kernel_headers_custom.tbz2 $DEVDIR/images/packages
rm -rf linux-headers-$KERNEL_MODULES_NAME

mkdir -p $DEVDIR/images/packages-backup
cp -rf $DEVDIR/kernel/* $DEVDIR/images/packages-backup

#TODO Esta sentencia ya está usada más abajo, hay que decidir donde la colocaremos finalmente
cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb

cd $DEVDIR/images
cp -rf arch/arm64/boot/Image arch/arm64/boot/zImage packages/kernel_supplements.tbz2 $DEVDIR/kernel/
cp -rf packages/kernel_headers_custom.tbz2 $DEVDIR/kernel/kernel_headers.tbz2

cd $DEVDIR/
sudo ./apply_binaries.sh

# Pasamos a usar el Jetpack para cargar lo necesario

cd $DEVDIR/bootloader/
mv system.img.raw system.img $DEVDIR/images/packages-backup/

# Ejecutamos el Jetpack
cd $DEVDIR/../../
./JetPack-L4T-3.2-linux-x64_b196.run

echo -n "Ponga la Jetson en modo depuración y pulse [ENTER] para continuar...: "
read var_name

cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb
cd $DEVDIR
sudo ./flash.sh -r -k kernel-dtb jetson-tx2 mmcblk0p1
