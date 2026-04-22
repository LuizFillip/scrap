import datetime as dt
import scrap as wb
import base as b 
                
                
dn = dt.datetime(2015, 12, 19)

def dn2fn(dn, code = 'slz'):

    return dn.strftime(f'{code}%d%b.%ym').lower()

def fn2dn(file, code = 'vss'):
    fmt = f'{code}%d%b.%ym'
    return dt.datetime.strptime(file, fmt)

codes = {
    'sao_luis': 'slz',
    'cachoeira': 'cxp',
    'vassouras': 'vss',
    'eusebio': 'eus'
    }

def download_magnetometer(
        ref, 
        save_in, 
        site  = "sao_luis"):

    url = wb.embrace_url(
            ref, 
            site = site, 
            inst = "magnetometer"
            )

    save_in = f'{save_in}{ref.year}'
    
    b.make_dir(save_in)
    
    code = codes[site]
    
    out = []
    for link in wb.request(url):    
        
        if code in link:
            dn = fn2dn(link, code = code)
            
            print('Downloading', link)
            wb.download(
                url, 
                link, 
                save_in
                )
    
            
    return None 



def main():
    ref = dt.datetime(2015, 12, 13)
    
    days = [13, 16, 18, 29, 19, 20, 21, 22]
    days = [3, 4, 30, 28]
    for site in ['sao_luis', 'eusebio']:
        download_magnetometer(ref, site)
    
# main()

        
# dowload_all_years(site = 'eusebio')

def download_data():
    site = 'eusebio'
    site_code = codes[site]
    
    save_in = f'magnet/data/2025/{site_code.upper()}'
    
    ref  = dt.datetime(2025, 1, 1)
    url = wb.embrace_url(
            ref, 
            site = site, 
            inst = "magnetometer"
            )
    
     
    b.make_dir(save_in)
    
    code = codes[site]
    
    out = []
    for link in wb.request(url):    
        
        if code in link:
          
            print('Downloading', link)
            wb.download(
                url, 
                link, 
                save_in
                )