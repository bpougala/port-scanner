import socket
import errno
from subprocess import check_output
from socket import error as socket_error

# this function scans all IP addresses present in the network and pings each of them individually at a given port.
# if it can download some data, it returns this IP address, assumed to be the one of the server. It returns 0 otherwise

class IPPortScanner():

    def __init__(self):
        print("[INFO] looking for a server...")

    def get_server(self, port):
        
        if port != int(port) or port < 0:
            return -1 
        hostname = socket.gethostname()
        pi_ip = socket.gethostbyname(hostname)

        #run nmap to scan all IP addresses on the network using 24 bits as the address range
        sub = check_output(['nmap', '-sL', '-n', pi_ip + '/24']).decode('utf8').splitlines()
        ip_list = list()
        for elem in sub:
            ip_list.append(elem[21:len(elem)]) # remove the heading of the response of the nmap call and only keep the IP
                                               # address itself

        for ip in ip_list[1:len(ip_list) - 2]: # loop over all IP addresses except our own
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05)
            try:
                result = sock.connect((ip, port))
                try:
                    get = check_output(['curl', ip + ":{port_n}".format(port_n=port)], timeout=0.05) # make a cURL call to port 8080 to see if it's open
                    if get != 0:
                        print("Found an IP address with port {port_n} open and sharing.".format(port_n=port))
                        return ip
                except Exception: # if an IP address has port 8080 closed, an exception will occur and must be ignored
                    continue
            except socket_error as serr:
                if serr.errno == 13:
                    print("An exception with error code 13 occured")
                    sock.close()
                    continue
                elif serr.errno != errno.ECONNREFUSED:
                    print("An exception occured")
                    sock.close()
                    continue
                else:
                    print("No connection at this address: %s" % ip)
                    sock.close()
                    continue

        return 0
