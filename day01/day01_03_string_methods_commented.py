# ============================================================
# Day01 任務 3：字串方法 —— 清理從設備抓回來的版本字串
# strip() 去頭尾空白、upper() 轉大寫、replace() 替換文字
# ============================================================

# 原始字串前後各有 2 個空格（從設備輸出抓下來常常會這樣）
version_raw = "  Cisco IOS XE Software, Version 17.03.04  "

# strip()：去掉「頭尾」的空白（中間的空白不會動）
aa = version_raw.strip()
print('去掉空格: '+aa)

# upper()：全部轉成大寫（lower() 則是轉小寫）
bb = aa.upper()
print('转大写:   '+bb)

# replace(舊, 新)：把字串裡的「舊」換成「新」
# 注意：字串不能直接修改，replace 會「回傳一個新字串」，所以要用變數接住
cc=aa.replace('17.03.04','17.06.01')
print('替换版本: '+cc)

# 執行結果：
# 去掉空格: Cisco IOS XE Software, Version 17.03.04
# 转大写:   CISCO IOS XE SOFTWARE, VERSION 17.03.04
# 替换版本: Cisco IOS XE Software, Version 17.06.01
