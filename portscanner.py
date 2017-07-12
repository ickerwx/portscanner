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

        def __hash__(self):
            return hash(tuple(sorted(self.__dict__.items())))


    def __init__(self, ip=None, hostname=None, ports=None):
        self.ip = ip

        if hostname is None:
            if self.ip is not None:
                try:
                    self.hostname, _, _ = socket.gethostbyaddr(self.ip)
                except:
                    self.hostname = None
            else:
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
        return "%s (%s)" % (self.hostname or "unknown", self.ip)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hostname == other.hostname and self.ip == other.ip and self.ports == other.ports
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class Scanner:
    def __init__(self, verbose=False, timeout=0.3):
        self.hosts = set()
        socket.setdefaulttimeout(timeout)
        self.verbose = verbose

    def getHost(self, ip):
        for host in self.hosts:
            if host.ip == ip:
                return host
        return None

    def discoverHosts(self, rangeprefix, discoveryPorts = [21, 22, 23, 25, 80, 139, 443, 445, 1521, 3306, 3389, 5432, 8080, 8443]):
        threads = []
        for i in range(1,255):
            existingHost = self.getHost(rangeprefix + str(i))
            host = existingHost if existingHost is not None else Host(ip=rangeprefix + str(i))
            t = threading.Thread(target=self.discoverSingleHost, args=(host, discoveryPorts))
            threads.append(t)
            t.start()

    def discoverSingleHost(self, host, discoveryPorts):
        for port in discoveryPorts:
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

    def scanSingleHost(self, host, ports):
        if self.verbose:
            print "Scanning", host
        for port in ports:
            t = threading.Thread(target=self.scanPort, args=(host, port))
            t.start()
        if self.verbose:
            print "Finished scanning", host

    def scanPort(self, host, port):
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


