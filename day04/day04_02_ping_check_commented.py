# ============================================================
# Day04 任務 2：pythonping —— 檢查主機是否可達
#
# 功能：
#   ping_check(host) ping 一台主機：
#     可達   → 回傳 (True, 平均 RTT 毫秒)
#     不可達 → 回傳 (False, None)
#   __main__ 依序檢查 3 台，印出「可达 / 不可达」
#
# 權限注意：
#   pythonping 要用 raw socket 自己組 ICMP 封包，Linux 只允許 root 這麼做。
#   一般帳號直接跑會出現 PermissionError: [Errno 1] Operation not permitted
#   解法二選一：
#     (1) sudo ~/ai-coding-day01/.venv/bin/python day04_02_ping_check.py
#     (2) 只給 Python 這一項權限（本機已設定，之後不用 sudo）：
#         sudo setcap cap_net_raw+ep <venv 的 python 實體路徑>
# ============================================================

from pythonping import ping

def ping_check(host, count=1, timeout=2):
    """ping通返回(True, 平均延迟毫秒)，不通返回(False, None)。"""

    # 使用函式的參數 count / timeout，不要寫死 → 呼叫者才能自訂
    # verbose=False → 不讓 pythonping 自己印出每個封包的結果
    rs = ping(host,count=count,timeout=timeout,verbose=False)

    # rs.success() 一定要加 ()：
    #   rs.success   → 「函式本身」，放在 if 裡永遠是 True（陷阱！）
    #   rs.success() → 呼叫函式，得到真正的 True / False
    if rs.success():
        # 有通才取 RTT；這個分支裡 rs.success() 一定是 True
        return(rs.success(),rs.rtt_avg_ms)
    else:
        # 不通時 rs.rtt_avg_ms 會是 timeout 的 2000（ms），不是真的 RTT，
        # 所以依規定回傳 None，避免呼叫者誤用
        return False,None

if __name__ == '__main__':
    hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']   # 10.1.1.3 不存在，用來測試「不可达」
    for host in hosts:
        # 函式回傳兩個值（tuple），用兩個變數一次接住（拆包 unpacking）
        ok, rtt = ping_check(host)
        if ok:
            # {rtt:.2f} → 數字格式化成小數點後 2 位（rtt 必須是數字，不能是字串）
            print(f'{host}   可达   RTT: {rtt:.2f} ms')
        else:
            print(f'{host}   不可达')
