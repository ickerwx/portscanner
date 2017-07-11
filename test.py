import portscanner as ps
s = ps.Scanner(verbose=False)
s.discoverHosts("192.168.1.")
print s.hosts
s.scanHosts(ports=[x for x in range(1,1000)])
for h in s.hosts:
    print h
    print h.ports
