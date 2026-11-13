# ============================================================
# Day01 任務 8：正則表達式 re.search() —— 從 Syslog 抓出介面和狀態
# ============================================================

import re      # 正則表達式模組（regular expression），Python 內建

# 一筆 Syslog 的各個欄位
date = "2026-03-03"
hostname = "SW-Core-01"
level = "CRITICAL"
message = "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"


# re.search(規則, 字串)：在整個字串裡「找」第一個符合規則的地方
#   （re.match 只從字串開頭比對，這裡訊息開頭是 %LINK...，所以要用 search）
# 規則前面加 r 代表原始字串，反斜線 \ 不會被 Python 先吃掉
#
# 規則拆解：Interface (\S+), changed state to (\S+)
#   Interface          → 照字面比對
#   (\S+)              → \S = 非空白字元，+ = 一個以上；( ) = 捕獲組，要抓出來的部分
#                        這裡抓到 "GigabitEthernet0/1"（遇到逗號前停止，因為後面要比對 ","）
#   , changed state to → 照字面比對
#   (\S+)              → 第 2 個捕獲組，抓到 "down"
m = re.search(r"Interface (\S+), changed state to (\S+)",message)

# m.group(1) = 第 1 個括號抓到的內容，m.group(2) = 第 2 個
# （group(0) 是整段比對到的文字）
# 如果沒比對到，m 會是 None，呼叫 .group() 就會報錯
interface = m.group(1)
status = m.group(2)

#print(Interface)
#print(Status)

# f-string 輸出
print(f"日期 : {date}" )
print(f"设备 : {hostname}")
print(f"等级 : {level}")
print(f"接口 : {interface}")
print(f"状态 : {status}")

# 執行結果：
# 日期 : 2026-03-03
# 设备 : SW-Core-01
# 等级 : CRITICAL
# 接口 : GigabitEthernet0/1
# 状态 : down
