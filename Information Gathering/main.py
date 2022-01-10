from directory_maker import *
from domain_name import *
from ip_address import *
from robots_txt import *
from who_is import *
from Dns_exploration import *
import sys
import socket
from datetime import datetime
from urllib.parse import urlparse
import re

ROOT_DIR = 'Info_gather'
create_dir(ROOT_DIR)

def gather_info(name, url):
    domain_name = get_domain_name(url)
    ip_address = get_ip_address(url)
    robots_txt = get_robots_txt(url)
    who_is = who_is_lookup(domain_name)
    create_report(name, url, domain_name, robots_txt, who_is)

def create_report(name, full_url, domain_name, robots_txt, who_is):
    project_dir = ROOT_DIR + '/' + name
    create_dir(project_dir)
    write_file(project_dir + '/full_url.txt', full_url)
    write_file(project_dir + '/domain_name.txt', domain_name)
    write_file(project_dir + '/robots_txt.txt', robots_txt)
    write_file(project_dir + '/who_is.txt', str(who_is))
    
def main():    
    link = input('Enter link (https) : ')
    parser = urlparse(link)
    url = 'https://' + parser.netloc
    if link != url:
        print('Please enter a valid link')
        print(url)
        print("-" * 50)
        link = input('Enter link (https) : ')
        if link != url:
            sys.exit()

    print("-" * 50)

    name = input('Enter the name : ')

    print("-" * 50)

    gather_info(name, link)

    print('Folder is Ready!!!')

    print("-" * 50)

    ip = get_ip_address(link)

    print("-" * 50)
    print("Scanning Target: " + ip)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)

    port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
    port_min = 0
    port_max = 65535
    open_ports = []

    while True:   
        print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
        port_range = input("Enter port range: ")
        port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
        if port_range_valid:
            port_min = int(port_range_valid.group(1))
            port_max = int(port_range_valid.group(2))
            break   
    
    for port in range(port_min, port_max + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        
                s.settimeout(1)
                s.connect((ip, port))
                open_ports.append(port)
        except:
            pass 
    
    for port in open_ports:
        print("Port {} is open on {}.".format(port, ip))
    
    print("-" * 50)

    ans = str(input("DNS Exploration (Y/N) : "))

    print("-" * 50)

    try:
        if ans == 'y' or ans == 'Y':
            textfile = "subdomain.txt"
            dictionary = []
            with open(textfile, "r") as f:
                dictionary = f.read().splitlines()
            domain = get_domain_name(link)
            SubdomainSearch(domain, dictionary, True)
        else:
            print('Thankyou')
    except KeyboardInterrupt:
        print ('Interrupted')

if __name__ == '__main__':
    main()
