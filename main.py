# coding: utf-8

import requests
import json
import geopandas as gpd
import pandas as pd
import zipfile, io
from os import listdir, getenv, mkdir, remove
import os
from os.path import isfile, join, isdir

def mk_dir(path):
    """"""
    if isdir(path) is False:
        mkdir(path)

def mk_dir_delete(path):
    """"""
    if isdir(path) is True:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            remove(join(path, file))
    else:
        mkdir(path)

    return

region = getenv('region')

mk_dir('data')
mk_dir('data/inputs')
mk_dir_delete('data/outputs')

out_dir = 'data/outputs'
input_dir = 'data/inputs'

# get list of files/geopackages
files = [f for f in listdir(join(input_dir)) if isfile(join(input_dir, f))]

for file in files:

    # read in geopackage into a dataframe
    gdf = gpd.read_file(join(input_dir, file))

    # drop any duplicate polygons
    gdf = gdf.drop_duplicates()

    # generate layer excluding toads
    gdf_nr = gdf[~gdf.theme.str.contains('Roads Tracks And Paths')]
    name = '%s_%s.gpkg' %(region, 'developed_exroads')
    gdf_nr.to_file(join(out_dir, name), driver='GPKG')

    # generate layer with only buildings
    gdf_blds = gdf[gdf['featurecode'] == 10021 ]
    name = '%s_%s.gpkg' % (region, 'buildings')
    gdf_blds.to_file(join(out_dir, name), driver='GPKG')

    # generate layer with only roads
    gdf_roads = gdf[gdf['featurecode'] == 10172 ]
    name = '%s_%s.gpkg' % (region, 'roads')
    gdf_roads.to_file(join(out_dir, name), driver='GPKG')
   
