# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 10:02:47 2026

@author: Luiz
"""

from tqdm import tqdm 
import base as b 

year = 2022
url = f'https://cdaweb.gsfc.nasa.gov/pub/data/icon/l2/l2-2_mighti_vector-wind-red/{year}/'

path_to_save = f'D:\\database\\icon\\{year}\\'

b.make_dir(path_to_save)

for href in tqdm(request(url)):
    
    if '.nc' in href:
        download(
            url, 
            href, 
            path_to_save
            )