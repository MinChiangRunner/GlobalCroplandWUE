#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@file        :WUEcalculate.py
@description :
@time        :2023/01/15 19:59:52
@author      :Jim Chiang
@version     :1.0
'''

import os
import re
import glob
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import date, datetime
import matplotlib.pyplot as plt
import time
import logging
import warnings
from functools import wraps
import rasterio as rio
import numpy as np
# %%


def read_raster(file, maskfile=None):
    with rio.open(file) as scr:
        meta = scr.meta
        Data = scr.read(1, masked=True)
    if np.ma.is_masked(Data):
        mask = Data.mask | np.isnan(Data)
    else:
        if np.isnan(Data[0, 0]):
            mask = np.isnan(Data)
        else:
            mask = (Data == Data[0, 0]) | np.isnan(Data)
    if maskfile:
        maskData, maskmeta = read_raster(maskfile)
        mask = maskData.mask | mask
    Data = np.ma.masked_where(mask, Data)
    return Data, meta
# %%


def write_raster(file, data, meta):
    if np.ma.is_masked(data):
        if meta.get('nodata'):
            data = data.filled(meta.get('nodata'))
        else:
            data = data.filled()
    with rio.open(file, 'w', **meta) as dst:
        dst.write(data, 1)

# %%

def WUE_Calculate(params):

    scalefactor = 0.01
    NPPfile, ETfile, WUEfile = params
    nppdata, nppmeta = read_raster(NPPfile)
    nppdata = np.ma.masked_where(
        nppdata.mask | (nppdata == 0), nppdata)
    # nppdata = np.ma.masked_where((nppdata == -1) | np.isnan(nppdata), nppdata)
    etdata, etameta = read_raster(ETfile)
    etdata = np.ma.masked_where(
        (etdata == -1) | (etdata == 0), etdata)
    # wue = np.float32(nppdata*scalefactor/etdata)

    wue = np.float32(nppdata*1./etdata)
    nppmeta.update(compress='lzw', nodata=-1, dtype='float32')
    # outfile = '/mnt/jim/XDA19030203Share/GPP/WUE_V2023/WUE_NPP_08/WUE.all.2001.test.tif'
    write_raster(WUEfile, wue, nppmeta)


if __name__ == "__main__":
    WUE_Calculate(params)
