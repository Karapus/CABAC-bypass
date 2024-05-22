#!/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

def readCSV(file):
    DF = pd.read_csv(file)
    DF["Bits"] = DF["Bytes"] * 8
    DF = DF.sort_values("Bits")
    CS = CubicSpline(y=np.log10(DF["Bits"]), x=DF["YUV_PSNR"])
    return (DF, CS)

ancorDF, ancorCS = readCSV("ancor.csv")
modifiedDF, modifiedCS = readCSV("modified.csv")
PSNR_range = np.arange(30, 44, 0.1)
plt.plot(np.log10(ancorDF["Bits"]), ancorDF["YUV_PSNR"], "ro", label="ancor")
plt.plot(ancorCS(PSNR_range), PSNR_range, "r--", label="ancor interpolation")
plt.plot(np.log10(modifiedDF["Bits"]), modifiedDF["YUV_PSNR"], "bo", label="modified")
plt.plot(modifiedCS(PSNR_range), PSNR_range, "b--", label="modified interpolation")
plt.xlabel("$log_{10}(Bits)$")
plt.ylabel("PSNR")
plt.legend()
plt.grid()
plt.savefig('BDRate.png')

D_l = 32
D_h = 41
BDRate = 10.0 ** ((modifiedCS.integrate(D_l, D_h) - ancorCS.integrate(D_l, D_h)) / (D_h - D_l)) - 1
print(f"BD-PSNR: {BDRate:.4}")
