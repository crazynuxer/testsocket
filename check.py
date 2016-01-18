#!/usr/bin/python
import socket

class check():
    def select_ip_version(host, port):
        """Returns AF_INET4 or AF_INET6 depending on where to connect to."""
        # disabled due to problems with current ipv6 implementations
        # and various operating systems.  Probably this code also is
        # not supposed to work, but I can't come up with any other
        # ways to implement this.
        ##try:
        ##    info = socket.getaddrinfo(host, port, socket.AF_UNSPEC,
        ##                              socket.SOCK_STREAM, 0,
        ##                              socket.AI_PASSIVE)
        ##    if info:
        ##        return info[0][0]
        ##except socket.gaierror:
        ##    pass
        if ':' in host and hasattr(socket, 'AF_INET6'):
            return socket.AF_INET6
        return socket.AF_INET

    def healthcheck(fam=socket.AF_INET,host,port):
        '''
        :param host: ip address
        :param port: port number, integer
        :return:
        '''
        sock = socket.socket(fam, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex((host,int(port)))
            if result == 0:
                return 'OK'
            else:
                return 'FAIL'
        except:
            pass
''' example '''
'''
if select_ip_version(host,port) == 10:
    healthcheck(fam=socket.AF_INET6, host,port)
else:
    healthcheck(host,port)
'''
