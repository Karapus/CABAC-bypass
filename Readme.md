# Replacing context bins with bypass bins in CABAC

## Building the software

To build the [HEVC Test Model](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/tree/master), with a newer compiler (GCC 13.2.1), it was necessary to disable `-Werror` flag, passed to compiler unconditionally.

This was done by [a patch to the build system](disable_warnings.patch).

## Collecting reference results

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
