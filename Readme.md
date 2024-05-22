# Replacing context bins with bypass bins in CABAC

## Building the software

To build the [HEVC Test Model](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/tree/master), with a newer compiler (GCC 13.2.1), it was necessary to disable `-Werror` flag, passed to compiler unconditionally.

This was done by [a patch to the build system](disable_warnings.patch).

## Collecting reference data

To collect necessary data a [Bash script](run-encoder.sh) was employed.

The script runs the encoder with QP values of 22, 27, 32, 37 on 9 frames of the input file and outputs YUV PSNR and number of bytes used in CSV format.
```
> run-encoder.sh \
        <PATH_TO_ENCODER> \
        <PATH_TO_INPUT_FILE> \
        <PATH_TO_CONFIG_FILE> \
        <SOURCE_WIDTH> \
        <SOURCE_HEIGHT> \
        <FRAME_RATE> \
        <INPUT_BIT_DEPTH> \
    > ancor.csv
```

The config used is [`encoder_randomaccess_main.cfg`](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/cfg/encoder_randomaccess_main.cfg).

The resulting CSV:
```
> cat ancor.csv
QP,YUV_PSNR,Bytes
22,40.1237,49902
27,36.7562,27766
32,33.8967,16145
37,31.3806,10015
```

## Modifying the software

Abstract interface of an encoder is defined in class `TEncBinIf` in [`HM/source/Lib/TLibEncoder/TEncBinCoder.h`](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncBinCoder.h).
The interface includes two functions that are relevant to the task at hand:
* [encodeBin()](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncBinCoder.h#L67) -- encodes a context bin.
* [encodeBinEP()]( https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncBinCoder.h#L68) -- encodes bypass bin.

The interface is implemented by classes [`TEncBinCABAC`](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncBinCoderCABAC.h#L47) and [`TEncBinCABACCounter`](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncBinCoderCABACCounter.h#L50) which inherits from `TEncBinCABAC` and speeds up calculations by usig look-up tables.

Which implementation is used depends on macro (`FAST_BIT_EST`)[https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibEncoder/TEncTop.h#L101-107].

`FAST_BIT_EST` is [unconditionaly defined to `1`](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/blob/fb4486d5ab5d0cd3b6a71659c7d5eb4509f2a4ce/source/Lib/TLibCommon/TypeDef.h#L132).

Therefore, the implementation from `TEncBinCABACCounter` is used and is the only one that needs to be modifyed.

This is done by [another patch](replace_context_with_bypass.patch).

## Collecting data for modifyed software

Done in a similar fashion:
```
> run-encoder.sh \
        <PATH_TO_ENCODER> \
        <PATH_TO_INPUT_FILE> \
        <PATH_TO_CONFIG_FILE> \
        <SOURCE_WIDTH> \
        <SOURCE_HEIGHT> \
        <FRAME_RATE> \
        <INPUT_BIT_DEPTH> \
    > modifyed.csv
```

The resulting CSV:
```
> cat modified.csv
QP,YUV_PSNR,Bytes
22,39.8368,49075
27,36.5680,27676
32,33.8599,16378
37,31.3112,10261
```

## Computing BD-rate

To compute the BD-rate a [Python script](getBDRate.py) is employed.

Resulting BD-PSNR difference is 0.02834.

![image](https://github.com/Karapus/CABAC-bypass/assets/45774052/e7ab6dc2-3eba-4f70-8ea2-32150f51e860)
