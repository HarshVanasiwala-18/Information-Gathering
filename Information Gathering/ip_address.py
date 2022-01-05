import socket
from domain_name import *

def get_ip_address(url):
    x = get_domain_name(url)
    ip = socket.gethostbyname(x)
    return ip



