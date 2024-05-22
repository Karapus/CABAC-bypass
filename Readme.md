# Replacing context bins with bypass bins in CABAC

## Building the software:

To build the [HEVC Test Model](https://vcgit.hhi.fraunhofer.de/jvet/HM/-/tree/master), with a newer compiler (GCC 13.2.1), it was necessary to disable `-Werror` flag, passed to compiler unconditionally.

This was done by [a patch to the build system](disable_warnings.patch).
