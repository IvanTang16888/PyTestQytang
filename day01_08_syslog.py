import re

date = "2026-03-03"
hostname = "SW-Core-01"
level = "CRITICAL"
message = "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"


m = re.search(r"Interface (\S+), changed state to (\S+)",message)

interface = m.group(1)
status = m.group(2)

#print(Interface)
#print(Status)

print(f"日期 : {date}" )
print(f"设备 : {hostname}")
print(f"等级 : {level}")
print(f"接口 : {interface}")
print(f"状态 : {status}")

