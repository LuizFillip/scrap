
import scrap as sp 
import base as b 
import datetime as dt 
from tqdm import tqdm 




 
def download_saber(dn):
    
    
    url = 'https://spdf.gsfc.nasa.gov//pub//data//timed//saber//level2a_netCDF//'
    
    month = dn.strftime('%Y//%j')
    url = url + month
    # print(url)
    save_in = 'D:\\database\\temp\\'
    
    b.make_dir(save_in)
    
    for ref in tqdm(sp.request(url), month):
       
        if ref.endswith('nc.gz'): 
            sp.download(url, ref, save_in)
    
    return None

def main():
 
    for i in range(1, 120):
        
        url = f'https://spdf.gsfc.nasa.gov/pub/data/timed/saber/level2a_netCDF/2025/{i:03d}/'
        
        save_in = 'D:\\database\\temp\\'
    
        for ref in tqdm(sp.request(url), str(i)):
           
            if ref.endswith('nc.gz'): 
                sp.download(url, ref, save_in)