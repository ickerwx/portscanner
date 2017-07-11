#!/usr/bin/env python2

import socket
import threading


class Host:
    class Portlist(set):
        def __str__(self):
            ports = list(self)
            retval = ""
            for p in ports:
                retval += str(p) + ', '
            return retval[: -2]

    def __init__(self, ip=None, hostname=None, ports=None):
        self.ip = ip

        if hostname is None:
            if self.ip is not None:
                try:
                    self.hostname, _, _ = socket.gethostbyaddr(self.ip)
                except:
                    self.hostname = None
        else:
            self.hostname = hostname
            if self.ip is None:
                self.ip = socket.gethostbyname(self.hostname)

        self.ports = Host.Portlist()
        if ports is not None:
            for p in ports:
                self.ports.add(int(p))

    def __str__(self):
        return "%s (%s)" % (self.hostname, self.ip)

    def __repr__(self):
        return self.ip


class Scanner:
    def __init__(self, verbose=False, timeout=0.3, portlist = [21, 22, 23, 25, 80, 139, 443, 445, 1521, 3306, 3389, 5432, 8080, 8443]):
        self.hosts = set()
        self.portlist = portlist
        socket.setdefaulttimeout(timeout)
        self.verbose = verbose

    def discoverHosts(self, rangeprefix):
        threads = []
        for i in range(1,255):
            host = Host(ip=rangeprefix + str(i))
            t = threading.Thread(target=self.discoverSingleHost, args=(host,))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    def discoverSingleHost(self, host):
        for port in self.portlist:
            try:
                s = socket.socket()
                s.connect((host.ip, port))
                # if we get here, the connection succeeded
                if self.verbose:
                    print 'Found', host, 'on', port
                s.close()
                host.ports.add(port)
                self.hosts.add(host)
                return
            except:
                pass

    def scanHosts(self, ports=None):
        if ports is None:
            ports = [x for x in range(1,65536)]
        threads = []
        for host in self.hosts:
            t = threading.Thread(target=self.scanSingleHost, args=(host,ports))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    def scanSingleHost(self, host, ports):
        if self.verbose:
            print "Scanning", host
        for port in ports:
            try:
                s = socket.socket()
                s.connect((host.ip, port))
                # if we get here, the connection succeeded
                if self.verbose:
                    print port, 'open on', host
                s.close()
                host.ports.add(port)
            except:
                pass
        if self.verbose:
            print "Finished scanning", host


