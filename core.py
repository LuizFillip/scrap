import os
import requests 
from bs4 import BeautifulSoup 
import urllib3
import socket
from urllib3.connection import HTTPConnection

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
        (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
        (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
        (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
    ]
)


HTTPConnection.default_socket_options = ( 
    HTTPConnection.default_socket_options + [
    (socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000), #1MB in byte
    (socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
])




def download(
        url: str, 
        href: str, 
        save_in: str = "", 
        verify = False
        ) -> str:
    
    """Function for download from link"""
    
    remote_file = requests.get(
        url + href, 
        verify = verify
        )
    
    path_to_save = os.path.join(save_in, href)
        
    with open(path_to_save, 'wb') as f:
        for chunk in remote_file.iter_content(
                chunk_size = 1024
                ): 
            if chunk: 
                f.write(chunk) 
                
    return path_to_save


def request(url, verify = False) -> list: 
    
    """Request website code source from url"""
    
    r = requests.get(url, verify = verify)
    s = BeautifulSoup(r.text, "html.parser")

    parser = s.find_all('a', href = True)

    return [link['href'] for link in parser]

def download_gold():
    url = 'https://spdf.gsfc.nasa.gov/pub/data/gold/level2/on2/2025/'
    
    save_in = 'D:\\database\\gold\\'
    
    for href in request(url):
        if 'nc' in href:
            print('downloading', href)
            download(url, href, save_in)