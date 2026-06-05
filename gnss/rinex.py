import scrap as wb
import GNSS as gs
import base as b 
import os
from tqdm import tqdm 
import calendar
import pandas as pd
import GEO as gg 

PATH_CHILE = 'D:\\database\\GNSS\\rinex\\chile\\'

networks = {
    "ibge" : 'https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados', 
    'igs': 'https://igs.bkg.bund.de/root_ftp/IGS/obs/',
    'chile': 'http://gps.csn.uchile.cl/data/', 
    'lisn': 'http://lisn.igp.gob.pe/jdata/database/gps/rinex/',
    'gage': 'https://gage-data.earthscope.org/archive/gnss/rinex/obs/',
    'garner': 'http://garner.ucsd.edu/pub/rinex/'
    }


def rinex_url(year, doy, network = "ibge"):
    date = gs.doy2date(year, doy)
    doy_str = date.strftime("%j")
    return f"{networks[network]}/{year}/{doy_str}/"




def convert_and_remove(path_to_save, files):
    root = path_to_save[:3]
    last = []
    msg = 'converting'
    for fn in tqdm(os.listdir(path_to_save), msg):
        path_in = os.path.join(path_to_save, fn)
        if fn not in files:
            wb.crx2rnx(path_in, root)
     
        if not fn.endswith('o'):
            last.append(path_in)
            
    
    for fn in last:
        os.remove(fn)
        
    return None
         
def filter_stations_by_latitude(latitude = -15):
 
    sites = gg.load_coords(2022)

    df = pd.DataFrame(sites).T

    df.columns = ['lon', 'lat', 'alt']
    
    return df.loc[df.lat > latitude].index

 

def download_routine(
        year, 
        doy,
        path_to_save,
        stations, 
        convert = False, 
        unzip = False
        ):
    
    b.make_dir(path_to_save) # criar o diretório do doy
    print('Starting RINEX', doy, year)
    download_rinex(
            year, 
            doy,
            path_to_save,
            stations,
            network = 'ibge',         
            )
    if unzip:
        files = uncompress(path_to_save)
        if convert:
            convert_and_remove(path_to_save, files) 
    return None 
 


def is_leap_year(year: int) -> bool:
    return calendar.isleap(year)

def days_in_year(year: int) -> int:
    return 366 if is_leap_year(year) else 365

def iter_doys(year: int, start_doy: int = 1, 
              end_doy: int | None = None):
    if end_doy is None:
        end_doy = days_in_year(year)
    start_doy = max(1, int(start_doy))
    end_doy = min(int(end_doy), days_in_year(year))
    return range(start_doy, end_doy + 1)

def locate_last_folder(path):
    # pega apenas pastas DOY numéricas (001..366)
    fns = [n for n in os.listdir(path.rinex) if n.isdigit()]
    to_nums = [int(n) for n in fns]
    return (1 if len(to_nums) == 0 else  (max(to_nums) + 1))  

def uncompress(path_root):
    unzip_msg = 'unzipping'
    files = []

    for fn in tqdm(os.listdir(path_root), unzip_msg):
        path_in = os.path.join(path_root, fn)

        try:
            if fn.endswith('.Z') or fn.endswith('d.Z'):
                wb.unzip_Z(path_in)
                files.append(fn)

            elif fn.endswith('.zip'):
                wb.unzip_zip(path_in)
                files.append(fn)

            elif fn.endswith('.gz'):
                wb.unzip_gz(path_in)
                files.append(fn)

        except Exception:
            continue

    return files

def download_rinex(
        year, 
        doy, 
        path_to_save, 
        stations = None, 
        network = 'ibge'
        ):
    url = rinex_url(year, doy, network)

    if stations is None:
        stations = []

    ends = ('.zip', 'd.Z', '.crx.gz', '.gz', '.Z')

    for href in tqdm(wb.request(url), desc="downloading"):
    
        if href[:4] in stations:
            if href.endswith(ends):
                wb.download(url, href, path_to_save)

    return None

def miss_receivers(year, doy):
    path = gs.paths(year, doy, root = 'D:\\')
    
    df = b.load(path.roti)
    
   
    stations = ['rnmo', 'pbcg', 
                'pepe', 'recf', 
                'rnna', 'pbjp', 'alar']

    return [s for s in stations if s not in df['sts'].unique()]


def download_rinex_daily(
        year, 
        stations, 
        root='C:\\', 
        resume=True, 
        start_doy=345, 
        end_doy=None
        ):
    path = gs.paths(year, root=root)

    b.make_dir(path.rinex_base)

    if resume:
        start_doy = locate_last_folder(path)

    for doy in iter_doys(
            year, 
            start_doy=start_doy, 
            end_doy=end_doy
            ):
        path_to_save = f"{path.rinex}{doy:03d}"
        # stations = miss_receivers(year, doy)

        download_routine(year, doy, path_to_save, stations)
        
 
def main_onew():
    doy = 366
    year = 2024
    path = gs.paths(year, root= 'F:\\')
    path_to_save = f"{path.rinex}{doy:03d}"
    
    
# year = 2026
# stations = filter_stations_by_latitude(latitude=-15)
# # download_routine(year, doy, path_to_save, stations)

# download_rinex_daily(
#         year, 
#         stations, 
#         root='E:\\', 
#         resume=True, 
#         start_doy=90, 
#         end_doy=None
#         )


# # stations
 
