
from __future__ import annotations
import gzip
import os
import shutil
import zipfile
from pathlib import Path
from typing import  Optional, Sequence, Union

from unlzw3 import unlzw


PathLike = Union[str, os.PathLike]


def _write_bytes(out_path: Path, data: bytes, overwrite: bool = True) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not overwrite:
        return out_path
    out_path.write_bytes(data)
    return out_path


def _write_text(out_path: Path, text: str, encoding: str = "utf-8", overwrite: bool = True) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists() and not overwrite:
        return out_path
    out_path.write_text(text, encoding=encoding, errors="replace")
    return out_path


def unzip_Z(
        path_in: PathLike, 
        encoding: str = "utf-8", 
        delete_input: bool = True) -> str:
    """
    Descompacta arquivo .Z (LZW) usando unlzw3 e grava o arquivo sem extensão .Z.
    Retorna o caminho do arquivo gerado.
    """
    in_path = Path(path_in)
    if in_path.suffix != ".Z":
        raise ValueError(f"Esperado arquivo .Z, mas recebi: {in_path}")

    raw = in_path.read_bytes()
    out_bytes = unlzw(raw)  # bytes

    out_path = in_path.with_suffix("")  # remove .Z

    # tenta gravar como texto (muito comum p/ orbit/ASCII), mas sem eval
    try:
        text = out_bytes.decode(encoding)
        _write_text(out_path, text, encoding=encoding)
    except UnicodeDecodeError:
        # se não for texto, salva binário
        _write_bytes(out_path, out_bytes)

    if delete_input:
        in_path.unlink(missing_ok=True)

    return str(out_path)


def unzip_orbit(
        path_in: PathLike, 
        path_to_save: PathLike, 
        encoding: str = "utf-8") -> str:
    """
    Descompacta um arquivo orbit .Z e salva no diretório path_to_save.
    Retorna o caminho do arquivo salvo.
    """
    in_path = Path(path_in)
    out_dir = Path(path_to_save)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = in_path.read_bytes()
    out_bytes = unlzw(raw)

    out_name = in_path.name.replace(".Z", "")
    out_path = out_dir / out_name

    try:
        _write_text(out_path, out_bytes.decode(encoding), encoding=encoding)
    except UnicodeDecodeError:
        _write_bytes(out_path, out_bytes)

    return str(out_path)


def unzip_zip(
        zip_path: PathLike, *, 
        extract_ext: Sequence[str] = ("o", "d")
        ) -> Optional[str]:
    """
    Extrai do .zip o primeiro arquivo cujo sufixo esteja em extract_ext (ex.: .o ou .d).
    Extrai no mesmo diretório do zip. Retorna o caminho extraído (ou None se não achou).
    """
    zpath = Path(zip_path)
    out_dir = zpath.parent

    with zipfile.ZipFile(zpath, "r") as zf:
        # tenta achar candidatos
        import re

        members = [
            n for n in zf.namelist()
            if re.search(r"\.\d{2}[do]$", n.lower())
        ]
        if not members:
            return None

        # pega o primeiro (ou você pode escolher a lógica "maior arquivo")
        member = members[0]
        zf.extract(member, out_dir)

    return str(out_dir / member)


def unzip_gz(infile: PathLike, *, delete_input: bool = False) -> str:
    """
    Descompacta .gz para o mesmo diretório.
    Retorna o caminho do arquivo descompactado.
    """
    in_path = Path(infile)
    if in_path.suffix != ".gz":
        raise ValueError(f"Esperado arquivo .gz, mas recebi: {in_path}")

    out_path = in_path.with_suffix("")

    with gzip.open(in_path, "rb") as f_in, open(out_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    if delete_input:
        in_path.unlink(missing_ok=True)

    return str(out_path)
