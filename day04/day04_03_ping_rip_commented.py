# ============================================================
# Day04 任務 3：先 ping 再 SSH —— 自動設定 RIP
#
# 功能：
#   依序處理 3 台設備：
#     ping 得通 → 用任務 1 的 qytang_multicmd SSH 進去送出 RIP 設定命令
#     ping 不通 → 直接跳過，完全不嘗試 SSH（10.1.1.3 不存在）
#
# 重點：用 import 重複使用前兩個任務的函式（不要複製貼上）
#   因為 day04_01 / day04_02 都有 if __name__ == '__main__':，
#   import 進來時只會拿到函式，不會執行它們的測試程式
#
# 驗證：跑完後登入路由器 → show running-config | section router rip
# ============================================================

from day04_01_multicmd import qytang_multicmd   # 任務 1：互動式 SSH 執行多條命令
from day04_02_ping_check import ping_check      # 任務 2：ping 檢查
import getpass

hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']    # C8Kv1、C8Kv2、不存在的主機
# RIP 設定命令：必須在「同一個互動終端」依序執行，
# 因為 router rip 要在 configure terminal 之後、version 2 要在 router rip 之下
RIP_COMMANDS = [
    'configure terminal',       # 進入全域設定模式      → C8Kv1(config)#
    'router rip',               # 進入 RIP 路由設定模式 → C8Kv1(config-router)#
    'version 2',                # 使用 RIPv2
    'network 172.16.0.0',       # 宣告 172.16.0.0 網段
    'end',                      # 回到特權模式          → C8Kv1#
]

if __name__ == '__main__':

    pwd = getpass.getpass('SSH密码:')        # 只問一次密碼，3 台共用

    for ip in hosts:                         # ip：這一圈的那一台（不是整個 hosts 清單）
        ok, rtt = ping_check(ip)             # 先 ping；只會拿到回傳值，函式內的 rs 在外面用不到（scope）
        if ok:
            # f'[{ip}]' 會代入 IP；後面的 ' ping通...' 是相鄰字串，Python 會自動接起來
            print(f'[{ip}]' ' ping通，开始配置RIP')
            # SSH 只能連一台 → 傳 ip，不是 hosts
            qytang_multicmd(ip,'admin',pwd,RIP_COMMANDS)
            print(f'[{ip}]' ' RIP命令执行完成')
        else:
            print(f'[{ip}]' ' ping不通，跳过SSH')     # 不通就跳過，不嘗試 SSH
