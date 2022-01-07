from directory_maker import *
from domain_name import *
from ip_address import *
from robots_txt import *
from who_is import *
from Dns_exploration import *
import sys
import socket
from datetime import datetime

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

    x = int(input('Starting Port : '))
    y = int(input('Ending Port : '))

    try:
        for port in range(x, y+1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((ip,port))
            if result ==0:
                print("Port {} is open".format(port))
            else:
                print("Port {} is close".format(port))
            s.close()

    except KeyboardInterrupt:
            print("\n Exiting Program !!!!")
            sys.exit()
    except socket.gaierror:
            print("\n Hostname Could Not Be Resolved !!!!")
            sys.exit()
    except socket.error:
            print("\ Server not responding !!!!")
            sys.exit()

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
