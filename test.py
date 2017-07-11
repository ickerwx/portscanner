import portscanner as ps
s = ps.Scanner(verbose=True)
s.discoverHosts("192.168.1.")
print s.hosts
s.scanHosts(ports=[x for x in range(1,1000)])
for h in s.hosts:
    print h, h.ports
