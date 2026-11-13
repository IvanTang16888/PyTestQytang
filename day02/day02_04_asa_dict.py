import re

asa_conn = """TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO
TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"""

asa_dict = {}

for line in asa_conn.split("\n"):

    m = re.match(r"\w+\s+\w+\s+(\S+):(\d+)\s+\w+\s+(\S+):(\d+),\s+idle\s+\S+,\s+bytes\s+(\d+),\s+flags\s+(\w+)", line)
    key = (m.group(1), m.group(2), m.group(3), m.group(4))
    value = (m.group(5), m.group(6))
    asa_dict[key] = value

print("打印分析后的字典!\n")
print(asa_dict)
print("\n格式化打印输出\n")

for key, value in asa_dict.items():
    print("{:<10}: {:<17}| {:<10}: {:<7}| {:<10}: {:<17}| {:<10}: {}".format(
        "src", key[0], "src_port", key[1], "dst", key[2], "dst_port", key[3]))
    print("{:<10}: {:<17}| {:<10}: {}".format("bytes", value[0], "flags", value[1]))
    print("=" * 84)
