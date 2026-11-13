import re

mac_table = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'

m = re.match(r"^(\d{1,4})\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+(\w+)\s+(\S+)$",mac_table)


print("{:<6}: {}".format("VLAN", m.group(1)))
print("{:<6}: {}".format("MAC",m.group(2)))
print("{:<6}: {}".format("Type",m.group(3)))
print("{:<6}: {}".format("Port",m.group(4)))
