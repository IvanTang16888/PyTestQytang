# ============================================================
# Day02 任務 4：把多行 ASA 連線資訊解析成「字典」
#   key   = (來源IP, 來源Port, 目的IP, 目的Port)   ← 元組
#   value = (bytes, flags)                        ← 元組
# ============================================================

import re

# 兩筆連線資料，用 """ 寫成多行字串
asa_conn = """TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO
TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"""

asa_dict = {}      # 先建立一個空字典，等一下逐行把結果放進去

# split("\n")：用換行符號把字串切成列表，一個元素 = 一行
for line in asa_conn.split("\n"):

    # 規則拆解（共 6 個捕獲組）：
    #   \w+\s+\w+\s+          → "TCP Student "（不用抓）
    #   (\S+):(\d+)           → 組 1 來源 IP、組 2 來源 Port
    #   \s+\w+\s+             → " Teacher "（不用抓）
    #   (\S+):(\d+),          → 組 3 目的 IP、組 4 目的 Port，後面接逗號
    #   \s+idle\s+\S+,        → "idle 0:00:00,"（不用抓）
    #   \s+bytes\s+(\d+),     → 組 5 bytes 數字
    #   \s+flags\s+(\w+)      → 組 6 flags（UIO）
    m = re.match(r"\w+\s+\w+\s+(\S+):(\d+)\s+\w+\s+(\S+):(\d+),\s+idle\s+\S+,\s+bytes\s+(\d+),\s+flags\s+(\w+)", line)

    # 用小括號 ( ) 把多個值包成「元組」tuple
    # 元組不能修改，所以可以當字典的 key（列表不行）
    key = (m.group(1), m.group(2), m.group(3), m.group(4))
    value = (m.group(5), m.group(6))

    # 字典[key] = value → 新增一筆資料
    asa_dict[key] = value

# 第 1 部分：直接印出整個字典
print("打印分析后的字典!\n")      # \n = 換行，多空一行
print(asa_dict)
print("\n格式化打印输出\n")

# 第 2 部分：格式化輸出
# .items() 一次取出 (key, value)，分別放進兩個變數
for key, value in asa_dict.items():
    # key[0]~key[3] = 來源IP、來源Port、目的IP、目的Port
    # 每個 {:<N} 都是靠左佔 N 格，讓每一欄上下對齊
    # 太長的程式碼可以在括號裡直接換行，Python 會當作同一行
    print("{:<10}: {:<17}| {:<10}: {:<7}| {:<10}: {:<17}| {:<10}: {}".format(
        "src", key[0], "src_port", key[1], "dst", key[2], "dst_port", key[3]))
    # value[0] = bytes、value[1] = flags
    print("{:<10}: {:<17}| {:<10}: {}".format("bytes", value[0], "flags", value[1]))
    print("=" * 84)       # 分隔線：84 個等號

# 執行結果（節錄）：
# {('192.168.189.167', '32806', '137.78.5.128', '65247'): ('74', 'UIO'), ...}
# src       : 192.168.189.167  | src_port  : 32806  | dst       : 137.78.5.128     | dst_port  : 65247
# bytes     : 74               | flags     : UIO
# ====================================================================================
