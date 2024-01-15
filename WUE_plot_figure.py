#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@file        :WUE_Statisitc_process.py
@description :作图数据处理
@time        :2023/09/06 20:24:00
@author      :Jim Chiang
@version     :1.0
'''
# %%
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
# %%
# Read data
StatisVar = 'NPP_WUE'
filedir = r'...'
# 'Tropical', 'Arid', 'Temperate', 'Cold'
GCfile = os.path.join(
    filedir, '....xlsx')
GCdf = pd.read_excel(GCfile, sheet_name=StatisVar)
# %%
# 'Tropical', 'Arid', 'Temperate', 'Cold'
WORLDGCdf = GCdf.loc[(GCdf.Polygon == 'World') &
                     (GCdf.type == 'All Cropland'), ['year', 'median']]
TropicalGCdf = GCdf.loc[(GCdf.Polygon == 'Tropical') &
                        (GCdf.type == 'All Cropland'), ['year', 'median']]
AridGCdf = GCdf.loc[(GCdf.Polygon == 'Arid') &
                    (GCdf.type == 'All Cropland'), ['year', 'median']]
TemperateGCdf = GCdf.loc[(GCdf.Polygon == 'Temperate') &
                         (GCdf.type == 'All Cropland'), ['year', 'median']]
ColdGCdf = GCdf.loc[(GCdf.Polygon == 'Cold') &
                    (GCdf.type == 'All Cropland'), ['year', 'median']]

# %%
GLASSfile = os.path.join(
    filedir, 'GLASS', '...xlsx')
GLASSdf = pd.read_excel(GLASSfile, sheet_name=StatisVar)
GlassWORLDdf = GLASSdf.loc[(GLASSdf.Polygon == 'World') &
                           (GLASSdf.type == 'All Cropland'), ['year', 'median']]
TropicalGlassdf = GLASSdf.loc[(GLASSdf.Polygon == 'Tropical') &
                              (GLASSdf.type == 'All Cropland'), ['year', 'median']]
AridGlassdf = GLASSdf.loc[(GLASSdf.Polygon == 'Arid') &
                          (GLASSdf.type == 'All Cropland'), ['year', 'median']]
TemperateGlassdf = GLASSdf.loc[(GLASSdf.Polygon == 'Temperate') &
                               (GLASSdf.type == 'All Cropland'), ['year', 'median']]
ColdGlassdf = GLASSdf.loc[(GLASSdf.Polygon == 'Cold') &
                          (GLASSdf.type == 'All Cropland'), ['year', 'median']]

# %%
MODISfile = os.path.join(
    filedir, 'MODIS', '..xlsx')
MODISdf = pd.read_excel(MODISfile, sheet_name=StatisVar)
# %%


# Figure Anomaly time series 
def plot_MODIS_GC_TimesSeries_Anomaly(figfile=None):
    valueField='mean' # 'median
    cm = 1/2.54
    fig, axs = plt.subplots(
        nrows=3, ncols=2, sharey='all', sharex='all', figsize=(18*cm, 16*cm), constrained_layout=True)
    FigNum = [chr(i) for i in range(65, 70)]
    for i in range(0, 5):
        ax = axs.flatten()[i]
        climatezone = ['World', 'Tropical', 'Arid',
                       'Temperate', 'Cold', 'Polar'][i]
        climatezoneName = ['Global', 'Tropical', 'Arid',
                           'Temperate', 'Cold', 'Polar'][i]
        GCdata = GCdf.loc[(GCdf.Polygon == climatezone) &
                          (GCdf.type == 'All Cropland'), ['year', valueField]]
        Glassdata = GLASSdf.loc[(GLASSdf.Polygon == climatezone) &
                                (GLASSdf.type == 'All Cropland'), ['year', valueField]]

        MODISdata = MODISdf.loc[(MODISdf.Polygon == climatezone) &
                                (MODISdf.type == 'All Cropland'), ['year', valueField]]

        GCdataWUE = GCdata[valueField].values
        GCWUEanomly = (GCdataWUE - np.mean(GCdataWUE))/np.mean(GCdataWUE)

        GLASSdataWUE = Glassdata[valueField].values
        GLASSWUEanomly = (GLASSdataWUE - np.mean(GLASSdataWUE)) / \
            np.mean(GLASSdataWUE)

        MODISdataWUE = MODISdata[valueField].values
        MODISWUEanomly = (MODISdataWUE - np.mean(MODISdataWUE)) / \
            np.mean(MODISdataWUE)

        lineGC, = ax.plot(GCdata['year'].values,
                          GCWUEanomly, '-o', color=(79/255., 120/255., 169/255.), 
                          markerfacecolor='white', markeredgewidth=2,label='GCWUE')
        lineGLASS, = ax.plot(Glassdata['year'].values,
                             GLASSWUEanomly, '-o', color=(235/255., 143/255., 107/255.), 
                             markerfacecolor='white', markeredgewidth=2,label='GLASS WUE')
        lineMODIS, = ax.plot(MODISdata['year'].values,
                             MODISWUEanomly, '-o', markeredgewidth=2,color=(84/255., 163/255., 79/255.), 
                             markerfacecolor='white', label='MODIS WUE')
        ax.text(2001, 0.13, s='({}) {}'.format(
            FigNum[i], climatezoneName), fontsize=14, family='Calibri')
        ax.set_xticks(GCdata['year'].values)
        # ax.set_xticks(np.arange(2001, 2021), labels=[
        #               '2001', '', '2003', '', '2005',  '', '2007', '',  '2009',  '', '2011',  '', '2013',
        #               '',  '2015',  '', '2017',  '', '2019',  '2020'])
        # ax.set_xlabel([str(i) for i in range(2001, 2021, 2)])
        # ax.set_yticks(np.arange(-40, 100, 50)/100.)
        ax.set_yticks([-0.2, -0.1, 0, 0.1, 0.2])
        ax.set_ylim((-0.2, 0.2))
        ax.tick_params(axis='x', labelrotation=90, labelsize=10)
        # if (i in np.arange(0, 3)):
        #     ax.tick_params(axis="x", labelbottom=False)
        if np.mod(i, 2) == 0:
            ax.set_ylabel(
                'Water-use efficiency \n Anomaly', fontsize=13, family='Calibri')
    axs[2, 1].remove()
    yearsLabel = [str(i) for i in np.arange(2001, 2021)]

    # 设置（1,1)位置图的横坐标标签
    for i in range(0, 20):
        fig.text(0.5855 + i*0.0195, 0.342,
                 yearsLabel[i], fontsize=10, rotation=90)

    # 设置图例
    fig.legend([lineGC, lineGLASS, lineMODIS], ['GCWUE', 'GLASS WUE', 'MODIS WUE'],
               ncol=1, bbox_to_anchor=(0.85, 0.3),
               fontsize=13, frameon=False)

    # 紧凑模式
    fig.tight_layout()
    if figfile:
        plt.savefig(figfile, dpi=300)
    plt.close()

figfile = r'WUE_Anomaly_timeseries.jpg'
plot_MODIS_GC_TimesSeries_Anomaly(figfile=figfile)
