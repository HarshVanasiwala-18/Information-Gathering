import dns
import dns.resolver
import socket

def ReverseDNS(ip):
    list = []
    try:
        result = socket.gethostbyaddr(ip)
        list.append(result[0])
        list.append(result[1])
        return list
    except socket.herror:
        return None

def DNSRequest(domain):
    ips = []
    try:
        result = dns.resolver.resolve(domain)
        if result:
            print(domain)
            for answer in result:
                print(answer)
                print("Domain Names: %s" % ReverseDNS(answer.to_text()))
    except (dns.resolver.NXDOMAIN, dns.exception.Timeout):
        return []
    return ips

def SubdomainSearch(domain, dictionary, nums):
    for word in dictionary:
        subdomain = word+"."+domain
        DNSRequest(subdomain)
        if nums:
            for i in range(0,10):
                s = word+str(i)+"."+domain
                DNSRequest(s)

 
