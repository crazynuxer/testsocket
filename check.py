#!/usr/bin/python
import socket

class check():
    def healthcheck(self,host,port,fam=socket.AF_INET):
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
    def servicecheck(self,host,port):
        ''' 
        :param host: ip address
        :param port: port number, integer
        :return:
        '''
        if ':' in host and hasattr(socket, 'AF_INET6'):
            return self.healthcheck(host,port,socket.AF_INET6)
        return self.healthcheck(host,port)
