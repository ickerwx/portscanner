# portscanner
Python port scanner and host discovery tool, using only the python standard library

```python
import portscanner
scanner = portscanner.Scanner()
scanner.discoverHosts("192.168.1.")
scanner.scanHosts()

for h in scanner.hosts:
    print h, h.ports
```
This is, for now, a dirty prototype, because I needed a python-based portscanner and host discovery tool.
I will implement proper IP handling next, but because of reasons I am for now limited to what is included in jython.
