# System Architecture

## Context

This project develops the hardware and software required to operate a multi-camera array around the NVIDIA Jetson TX2 platform.

The system combines mechanical design, custom electronics, embedded Linux configuration, image capture and computer vision processing.

## System view

```mermaid
flowchart LR
    SCENE[Scene] --> CAM[Camera sensors]
    CAM --> PCB[Camera and bridge electronics]
    PCB --> JETSON[NVIDIA Jetson TX2]

    MECH[Mechanical camera array] --> CAM
    ADJ[Camera angle adjustment] --> MECH

    JETSON --> DT[Kernel and Device Tree configuration]
    DT --> DRV[Camera drivers]
    DRV --> GST[GStreamer capture pipeline]

    GST --> RAW[Multi-camera image capture]
    RAW --> CAL[Camera array calibration]
    CAL --> DISP[Disparity estimation]
    DISP --> OUT[Depth-related results]
```

## Engineering domains

```mermaid
flowchart TD
    SYS[Multi-camera system]

    SYS --> ME[Mechanical]
    SYS --> EE[Electronics]
    SYS --> SW[Embedded software]
    SYS --> CV[Computer vision]

    ME --> ARRAY[Camera array structure]
    ME --> ANGLE[Camera angle adjustment]
    ME --> FAB[3D printed parts and drawings]

    EE --> MODULES[Camera and bridge modules]
    EE --> DEBUG[Debug hardware]
    EE --> FABPCB[PCB fabrication files]

    SW --> KERNEL[Kernel build scripts]
    SW --> DTS[Device Tree modifications]
    SW --> SENSOR[IMX219 support]
    SW --> GSTREAMER[GStreamer RAW10 patches]
    SW --> GPIO[Auvidea J20 GPIO setup]

    CV --> CAPTURE[Multi-camera capture]
    CV --> CALIBRATION[Software calibration]
    CV --> DISPARITY[Disparity maps]
```

## Mechanical subsystem

The mechanical design provides:

- the main camera array structure
- camera positioning and support
- adjustable camera angle mechanisms
- parts used during physical calibration
- manufacturing files and 3D-printing parameters

Relevant repository area:

`Desarrollo_Mecanico/`

## Electronics subsystem

The electronics work includes several iterations of camera, bridge, debugging and fabrication-oriented modules.

The repository contains design sources and manufacturing-related files for:

- OV5680 camera modules
- bridge modules
- Raspberry Pi camera sensor adaptation
- debug boards
- CNC fabrication tests
- Jetson support hardware

Relevant repository area:

`Desarrollo_Electronico/`

## Embedded software subsystem

The Jetson TX2 software work includes low-level platform adaptation required to operate the camera hardware.

The repository contains:

- original Jetson TX2 device tree resources
- Device Tree modifications
- IMX219 sensor driver modifications
- kernel compilation scripts
- GStreamer RAW10-related patches
- Auvidea J20 setup scripts
- GPIO configuration utilities

Relevant repository area:

`Desarrollo_Software/`

## Image-processing workflow

The project does not stop at camera bring-up. Captured images are used as the input to a computer-vision workflow.

```mermaid
flowchart LR
    C1[Camera 1] --> SET[Multi-camera capture]
    C2[Camera 2] --> SET
    C3[Camera 3] --> SET
    C4[Camera 4] --> SET
    C5[Camera 5] --> SET
    C6[Camera 6] --> SET

    SET --> CAL[Array calibration]
    CAL --> RECT[Geometric correspondence]
    RECT --> DISP[Disparity estimation]
    DISP --> RESULT[Experimental results]
```

Example capture sets are stored under `Array_captures/`, while representative outputs are available under `images/Resultados/`.

## Architecture significance

The main engineering challenge is the integration across domains.

Camera operation depends simultaneously on:

- mechanical alignment
- electrical compatibility
- sensor and carrier-board interfaces
- Linux kernel and Device Tree configuration
- image transport
- calibration quality
- image-processing algorithms

The project therefore represents a complete multidisciplinary engineering chain rather than an isolated software or hardware prototype.

## Historical platform note

This work was developed in 2018 around the NVIDIA Jetson TX2 ecosystem and the software stack available at that time.

Kernel, JetPack, driver and GStreamer details should be treated as historical technical material. They are valuable as implementation references, but they should not be assumed to apply directly to current Jetson platforms or software releases.
