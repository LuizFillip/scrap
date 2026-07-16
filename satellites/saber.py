from pathlib import Path
from datetime import datetime, timedelta
import gzip
import shutil
from tqdm import tqdm

import scrap as sp
import base as b


BASE_URL = "https://spdf.gsfc.nasa.gov/pub/data/timed/saber/level2a_netCDF"


def daterange(start_date, end_date):
    dn = start_date
    while dn <= end_date:
        yield dn
        dn += timedelta(days=1)


def gunzip_file(gz_file, remove_gz=True):
    gz_file = Path(gz_file)
    nc_file = gz_file.with_suffix("")  # remove .gz

    if nc_file.exists():
        gz_file.unlink()
        return nc_file

    with gzip.open(gz_file, "rb") as f_in:
        with open(nc_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    if remove_gz:
        gz_file.unlink()

    return nc_file


def download_saber_day(dn, save_in, unzip=True):
    save_in = Path(save_in)
    b.make_dir(save_in)

    year = dn.strftime("%Y")
    doy = dn.strftime("%j")

    url = f"{BASE_URL}/{year}/{doy}/"

    try:
        refs = sp.request(url)
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

    downloaded = []

    for ref in tqdm(refs, desc=f"{year}-{doy}"):
        if not ref.endswith(".nc.gz"):
            continue

        gz_path = save_in / ref
        nc_path = gz_path.with_suffix("")

        if nc_path.exists():
            continue

        if not gz_path.exists():
            try:
                sp.download(url, ref, str(save_in))
            except Exception as e:
                print(f"Erro ao baixar {ref}: {e}")
                continue

        if unzip and gz_path.exists():
            try:
                nc_path = gunzip_file(gz_path, remove_gz=True)
            except Exception as e:
                print(f"Erro ao descompactar {gz_path.name}: {e}")
                continue

        downloaded.append(nc_path if unzip else gz_path)

    return downloaded


def download_saber(
        start_date, 
        end_date, 
        save_in=r"D:\database\temp", 
        unzip=True
        ):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    all_files = []

    for dn in daterange(start_date, end_date):
        files = download_saber_day(dn, save_in, unzip=unzip)
        all_files.extend(files)

    return all_files

def main():
    
    files = download_saber(
        start_date="2024-01-01",
        end_date="2024-05-01",
        save_in=r"D:\database\SABER\2024",
        unzip=True
    )