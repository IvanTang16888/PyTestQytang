# ============================================================
# Day04 任務 1：Paramiko 互動式 Shell —— 同一個 SSH 連線依序執行多條命令
#
# 功能：
#   SSH 登入 C8Kv1（10.1.1.1），在「同一個互動終端」依序送出 cmd_list 的每條命令，
#   把所有回顯累加起來回傳；verbose=True 時邊執行邊印出來。
#
# exec_command() 和 invoke_shell() 的差別？
#   exec_command()：每條命令開一個新的通道，執行完就結束
#                   → 前一條命令的狀態（例如 terminal length 0、configure terminal）
#                     不會延續到下一條
#   invoke_shell() ：開一個「互動式終端」，就像你用 MobaXterm 登入後一行一行打字
#                   → 所有命令共用同一個 session，狀態會延續（任務 3 設定 RIP 就靠這點）
# ============================================================

import time, paramiko,getpass
# time    ：time.sleep() 暫停，等設備把回顯送回來
# paramiko：Python 的 SSH 函式庫
# getpass ：輸入密碼時畫面不顯示，比把密碼寫死在程式裡安全

# 要執行的命令清單（給下面 __main__ 測試用）
cmd_list = [
    'terminal length 0',                        # 取消分頁，避免輸出卡在 --More--
    'show version | include Software,',         # 只顯示含 "Software," 的那行 → IOS XE 版本
    'show running-config | include hostname',   # 只顯示 hostname 那行
]

# 參數說明：
#   ip, username, password：SSH 登入資訊
#   cmd_list ：要依序執行的命令（list）
#   wait_time：每送出一條命令後等幾秒再收回顯，預設 2 秒
#   verbose  ：True → 邊執行邊印出回顯；False → 不印，只回傳
def qytang_multicmd(ip,username,password,cmd_list, wait_time=2 , verbose=True):
    """在同一个SSH交互终端依次执行cmd_list，返回全部回显文本。"""

    # 1. 建立 SSH 用戶端
    ssh = paramiko.SSHClient()
    # 第一次連線時，設備的 host key 不在 known_hosts 裡 → 自動接受（lab 環境方便用）
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 2. 連線
    #    注意：一定要用「關鍵字參數」username= / password=
    #    因為 connect() 的第 2 個位置參數是 port，不是 username
    #    look_for_keys=False / allow_agent=False → 不嘗試 SSH 金鑰，直接用密碼登入
    ssh.connect(ip,username=username,password=password,look_for_keys=False, allow_agent=False)

    # 3. 開一個互動式終端（就像用 MobaXterm 登入後看到的畫面）
    chan = ssh.invoke_shell()
    # 等 1 秒，把登入時的歡迎訊息（banner、第一個提示符號）先收掉，
    # 不然它會混進第一條命令的回顯裡
    time.sleep(1); welcome = chan.recv(65535)

    output = ''                                  # 用來累加所有回顯的空字串
    for cmd in cmd_list:                         # 每一圈取出一條命令
        # sendall 只接受 bytes：
        #   cmd + '\n'  → 加上換行，等於按下 Enter
        #   .encode()   → 字串（str）轉成 bytes
        chan.sendall((cmd +'\n').encode())
        time.sleep(wait_time)                    # 等設備執行並送回結果
        # recv(65535)：一次最多收 65535 bytes；.decode()：bytes 轉回字串
        result = chan.recv(65535).decode()
        output += result                         # 累加到總輸出
        if verbose:                              # 在迴圈「裡面」→ 每條命令都會印
            print(result)
    # 迴圈結束（所有命令都跑完）才關閉連線並回傳 → 縮排跟 for 對齊
    ssh.close()
    return output                                # 回傳全部回顯（str），讓呼叫的人可以再處理


# 直接執行這個檔案時才會跑下面的測試；
# 被別的檔案 import（例如任務 3）時不會執行
if __name__ == '__main__':
    pwd = getpass.getpass('SSH密码:')            # 輸入密碼時畫面不會顯示任何字
    qytang_multicmd('10.1.1.1', 'admin', pwd, cmd_list)
