# ============================================================
# Day02 任務 2：正則解析 ASA 防火牆 show conn 的一行
# 抓出：協定、Server IP/Port、Client IP/Port
# ============================================================

import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

# 規則拆解（共 5 個捕獲組）：
#   (\w+)                                  → 組 1：協定 TCP
#   \s+server\s+                           → 字面 "server"，前後是空白（原始資料有 2 個空格，所以用 \s+）
#   (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   → 組 2：Server IP，4 段 1~3 位數字，中間用 \. 隔開
#   :                                      → 字面冒號
#   (\d+)                                  → 組 3：Server Port
#   \s+localserver\s+                      → 字面 "localserver"
#   (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})   → 組 4：Client IP
#   :(\d+)                                 → 組 5：Client Port
# 後面的 idle / bytes / flags 不需要，所以規則寫到這裡就結束（re.match 不要求比對到結尾）
m = re.match(r"(\w+)\s+server\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\s+localserver\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)", conn)

# {:<12} → 標題靠左佔 12 格（"Client Port" 是 11 個字元，12 格放得下）
print("{:<12}: {}".format("Protocol", m.group(1)))
print("{:<12}: {}".format("Server IP", m.group(2)))
print("{:<12}: {}".format("Server Port", m.group(3)))
print("{:<12}: {}".format("Client IP", m.group(4)))
print("{:<12}: {}".format("Client Port", m.group(5)))

# 執行結果：
# Protocol    : TCP
# Server IP   : 172.16.1.101
# Server Port : 443
# Client IP   : 172.16.66.1
# Client Port : 53710
