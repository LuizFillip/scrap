from __future__ import annotations
import datetime as dt
from pathlib import Path
from typing import Iterable, Sequence, Tuple, Union, Optional, List
import pandas as pd
from tqdm import tqdm
from base import make_dir
import scrap as wb
 
 
SITES = {
    "fortaleza": "FZA0M",
    "sao_luis": "SAA0K",
    "belem": "BLJ03",
    "cachoeira": "CAJ2M",
    "santa_maria": "SMK29",
    "boa_vista": "BVJ03",
    "campo_grande": "CGK21",
}


def sites_codes(site: str) -> str:
    try:
        return SITES[site]
    except KeyError as e:
        raise KeyError(f"Site desconhecido: {site}. Opções: {list(SITES)}") from e


def folder_name(dn: dt.datetime, site: str, flat: bool = False) -> str:
    """
    Ex:
      flat=False -> \\YYYY\\YYYYMMDDXX
      flat=True  -> YYYYMMDDXX
    onde XX = 2 letras do código do site (ex: FZ, SA, ...)
    """
    ext = sites_codes(site)[:2].upper()
    return dn.strftime(f"%Y%m%d{ext}") if flat else dn.strftime(f"{Path(str(dn.year)) / (dn.strftime(f'%Y%m%d{ext}'))}")


def fn2dt(filename: str) -> dt.datetime:
    """
    Ex: 'FZA0M_2015365210000.SAO' -> datetime pelo padrão %Y%j%H%M%S.
    """
    # mais robusto que split fixo
    parts = filename.split("_", 1)
    if len(parts) != 2:
        raise ValueError(f"Nome de arquivo inesperado: {filename}")

    date_part = parts[1].split(".", 1)[0]  # remove extensão
    return dt.datetime.strptime(date_part, "%Y%j%H%M%S")


def periods_by_range(
        start: dt.datetime, 
        hours: float = 24, 
        freq: str = "10min"
        ) -> pd.DatetimeIndex:
    end = start + dt.timedelta(hours=hours)
    return pd.date_range(start, end, freq=freq)


def periods_by_freq(
        start: dt.datetime, 
        end: Optional[dt.datetime] = None, 
        freq: str = "1D", 
        days: int = 150
        ) -> pd.DatetimeIndex:
    """
    Range por frequência. Se end=None, gera 1 ano a partir do start.
    """
    
    if end is None:
        end = start + dt.timedelta(days=days)
    return pd.date_range(start, end, freq=freq)


def create_folder_by_date(
        start: dt.datetime, 
        site: str, 
        root: Union[str, Path] = "D"
        ) -> Path:
    """
    Cria: <root>:/ionogram/YYYY/YYYYMMDDXX
    """
    root = (Path(f"{root}:\\") 
            if isinstance(root, str) 
            and len(root) == 1 else Path(root))
    base_dir = root / "ionogram" / str(start.year)
    make_dir(str(base_dir))
    save_in = base_dir / folder_name(
        start, site=site, flat=True)
    make_dir(str(save_in))
    return save_in


def _normalize_ext(
        ext: Union[str, Sequence[str]]) -> List[str]:
    if isinstance(ext, str):
        return [ext]
    return list(ext)


# ---------------------------- 
def filter_extensions(
    dn: dt.datetime,
    site: str = "sao_luis",
    ext: Union[str, Sequence[str]] = ("SAO", "RSF"),
) -> Tuple[str, List[str]]:
    """
    Retorna (url, [filenames]) para o timestamp dn.
    """

    exts = _normalize_ext(ext)
    exts = [e.upper() for e in exts]

    url = wb.embrace_url(dn, site=site, inst="ionosonde")

    files_filtered: List[str] = []

    for link in wb.request(url):
        link_up = link.upper()

        # ignorar arquivos XML e TMP
        if any(bad in link_up for bad in ("XML", "TMP")):
            continue

        # filtrar extensões desejadas
        if any(e in link_up for e in exts):
            files_filtered.append(link)

    return url, files_filtered
# ----------------------------
# Download routine
# ----------------------------

def download_in_day(
        dn_py, site, ext, 
        save_in,
        strict_timestamp_match: bool = True
        ):
    url, files = filter_extensions(dn_py, site=site, ext=ext)
    
    for filename in files:
        out_path =  Path(save_in) / filename
        if out_path.exists():
        
            continue

        if strict_timestamp_match:
            try:
                if fn2dt(filename) != dn_py:
                    continue
            except ValueError:
                # nome não bate padrão -> ignora
                continue

        try:
            wb.download(url, filename, str(save_in))
            
        except Exception:
            # se quiser logar, coloque print/ logger aqui
            continue
        
def download_ionograms(
    periods: Iterable[dt.datetime],
    site: str = "sao_luis",
    ext: Union[str, Sequence[str]] = ("SAO", "RSF"),
    root_drive: Union[str, Path] = "E",
    strict_timestamp_match: bool = True,
    save_in =  None
) -> None:
    """
    Baixa ionogramas para cada datetime em `periods`:
    - lista arquivos no servidor
    - filtra por extensão
    - opcionalmente baixa só se fn2dt(filename) == dn
    - salva em pasta por ano/data+site
    """
    if not isinstance(periods, dt.datetime):
        start = periods[0].to_pydatetime()
        
    if save_in is None:
        save_in = create_folder_by_date(
            start, 
            site = site, 
            root = root_drive
            )

    if isinstance(periods, dt.datetime):
       
        dn_py = periods
        print('Downloading', dn_py.strftime('%Y-%m-%d %H:%M'))
        download_in_day(
                dn_py, site, ext, 
                save_in,
                strict_timestamp_match = True
                )
    else:
        periods = pd.DatetimeIndex(periods)
        desc = f"{start:%Y-%m-%d} - {site}"
        for dn in tqdm(periods, desc=desc):
            dn_py = dn.to_pydatetime()
            
            download_in_day(
                    dn_py, site, ext, 
                    save_in,
                    strict_timestamp_match = True
                    )

            
def dn2fn(dn, ext = 'SAO'):
    
    fmt = f'SAA0K_%Y%j%H%M%S.{ext}'
    
    return dn.strftime(fmt)

    
 