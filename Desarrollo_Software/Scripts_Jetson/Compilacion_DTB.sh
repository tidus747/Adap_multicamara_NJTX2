#!/bin/bash

# Script para lanzar la compilación del DTB de la NVIDIA Jetson TX2
export DEVDIR=$HOME/JetPack-L4T-3.2/64_TX2/Linux_for_Tegra

export CROSS_COMPILE=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-
export CROSS32CC=/opt/linaro/gcc-linaro-5.3-2016.02-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-gcc
export KERNEL_MODULES_OUT=$DEVDIR/images/modules
export TEGRA_KERNEL_OUT=$DEVDIR/images
export ARCH=arm64

cd $DEVDIR/sources/kernel/kernel-4.4

make mrproper

make -j 2 O=$TEGRA_KERNEL_OUT tegra18_defconfig
make -j 2 O=$TEGRA_KERNEL_OUT menuconfig
make -j 2 O=$TEGRA_KERNEL_OUT dtbs

cp $DEVDIR/images/arch/arm64/boot/dts/tegra186-quill-p3310-1000-c03-00-base.dtb $DEVDIR/kernel/dtb

cd $DEVDIR

echo -n "Ponga la Jetson en modo depuración y pulse [ENTER] para continuar...: "
read var_name
sudo ./flash.sh -r -k kernel-dtb jetson-tx2 mmcblk1p1
