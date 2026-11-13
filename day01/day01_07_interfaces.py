# ============================================================
# Day01 任務 7：str.format() 對齊 —— 印出介面狀態表
# ============================================================

# 每個介面是一個字典：名稱、狀態、速率
interfaces = [
    {"name": "Gi0/0", "status": "up", "speed": "1G"},
    {"name": "Gi0/1", "status": "up", "speed": "1G"},
    {"name": "Gi0/2", "status": "up", "speed": "10G"},
    {"name": "Gi0/3", "status": "down", "speed": "10G"},
]

# 表頭
print("接口      状态    速率")
# 字串 * 數字 = 重複 N 次 → 印出 20 個 "-" 當分隔線
print("-"*20)

for interface in interfaces:
    # "模板".format(值1, 值2, 值3)：依序把值填進模板裡的 { }
    # {:<10} → 第 1 個值靠左、佔 10 格
    # {:<8}  → 第 2 個值靠左、佔 8 格
    # {}     → 第 3 個值原樣放進去
    # 這跟 f-string 的 {變數:<10} 效果一樣，只是寫法不同
    print("{:<10}{:<8}{}".format(interface["name"],interface["status"],interface["speed"]))

# 執行結果：
# 接口      状态    速率
# --------------------
# Gi0/0     up      1G
# Gi0/1     up      1G
# Gi0/2     up      10G
# Gi0/3     down    10G
