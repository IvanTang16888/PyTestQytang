import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

m = re.match(r"(\w+)\s+server\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s+localserver\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)", conn)

print("{:<12}: {}".format("Protocol", m.group(1)))
print("{:<12}: {}".format("Server IP", m.group(2)))
print("{:<12}: {}".format("Server Port", m.group(3)))
print("{:<12}: {}".format("Client IP", m.group(4)))
print("{:<12}: {}".format("Client Port", m.group(5)))
