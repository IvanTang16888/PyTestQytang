version_raw = "  Cisco IOS XE Software, Version 17.03.04  "
aa = version_raw.strip()
print('去掉空格: '+aa)
bb = aa.upper()
print('转大写:   '+bb)

cc=aa.replace('17.03.04','17.06.01')
print('替换版本: '+cc)
