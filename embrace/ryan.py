import pandas as pd 
import scrap as sp
from pathlib import Path 
import base as b 
import numpy as np             
import datetime as dt

def ryan_download():
    save_in = Path('E:\\iono_ssw\\')
         
    dates = [
        ['27/12/2012 00:00', '25/01/2013 00:00'],
        ['04/09/2013 00:00', '15/09/2013 00:00'], 
        ['01/02/2014 00:00', '13/02/2014 00:00'],
        ['19/02/2016 00:00', '26/03/2016 00:00'], 
        ['07/02/2018 00:00', '03/03/2018 00:00'], 
        ['2019-07-01 00:00', '2019-09-30 00:00'], 
        ['22/12/2020 00:00', '12/01/2021 00:00'], 
        ['03/07/2024 00:00',  '21/07/2024 00:00']
        ]
    
    import base as b 
    
    for ref in dates:
        start = pd.Timestamp(ref[0]) 
        end = pd.Timestamp(ref[1])
        
        save_in = save_in / start.strftime('%Y%m%d')
        
        b.make_dir(save_in)
        for dn in pd.date_range( start, end, freq = '10min'):
        
            
            sp.download_ionograms(
                dn, 
                site = 'sao_luis', 
                ext = ['SAO', 'RSF'], 
                save_in = save_in
                )
            
def dn2fn(dn, ext = 'SAO'):
    
    fmt = f'SAA0K_%Y%j%H%M%S.{ext}'
    
    return dn.strftime(fmt)



dates = ['2015-11-09', '2016-12-17', 
         '2018-02-13', '2018-12-04',
         '2018-12-05', '2019-01-30', 
         '2019-10-14', '2019-10-29',
         '2019-11-09', '2019-12-02', 
         '2020-03-05', '2020-09-29',
         '2022-11-07', '2023-04-08']


dates = ['2013-09-23', '2014-02-09', '2014-09-24', '2018-02-13',
               '2018-12-04', '2018-12-05', '2019-01-21', '2019-01-22',
               '2019-01-30', '2019-11-09', '2020-03-08', '2020-09-29']

dates = ['2024-03-21', '2024-03-24', '2024-04-04',
         '2024-04-09',
'2024-04-10', '2024-08-16', '2024-08-17', '2024-08-23',
'2024-09-12', '2024-10-07']



year = 2024
dates = pd.date_range(  f'{year}-01-01', 
                      f'{year}-12-31', 
                      freq = '1D')



# for ref in dates:

save_in = Path('D:\\ionogram\\miss\\2024\\')
 
 
# out = []
for ref in dates:
    ref = pd.Timestamp(ref)
    
    start = ref + dt.timedelta(hours = 20)
    end = start + dt.timedelta(hours = 3)
    
    
    for dn in pd.date_range( start, end, freq = '10min'):
     
        check_sup =  save_in  / dn2fn(dn, ext = 'SAO')
        
        # if not check_sup.exists():
            # print(ref)
        print('downloading', dn)
        sp.download_in_day(
                dn, 
                site = 'sao_luis', 
                ext = ('RSF', 'SAO'), 
                save_in = save_in  
                )
    