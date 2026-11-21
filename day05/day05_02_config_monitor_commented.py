# ============================================================
# Day05 任務 2：採集 show run → 算 SHA256 → 存資料庫 → 比較 → 有變化就告警
#
# 流程（每一輪）：
#   show run（qytang_multicmd） → 正則取出 hostname...end → SHA256（64 位 16 進位）
#   → 寫入一行（add + commit） → 查同一台設備最近兩筆（id 由新到舊）
#   → 比較 HASH：相同只印本次；不同就印告警 + 新舊兩次 HASH
#   → 等 5 秒，再來一輪（while True，按 Ctrl+C 停止）
#
# 3 個檔案協作（要放在同一個資料夾）：
#   day04_01_multicmd.py      → 第四天的互動式 SSH 函式
#   day05_01_router_model.py  → 任務 1 的 ORM 模型與 Session
#   本檔                      → 採集與比對
#
# 為什麼用 HASH？
#   整份設定 7000 多字，逐行比對很麻煩；SHA256 把它壓成 64 字元的「指紋」：
#   設定完全相同 → 指紋一定相同；只差一個字 → 指紋完全不同
#   （跟下載 IOS 後用 verify /md5 檢查檔案是同一個概念）
# ============================================================
"""第5天 · 任务2:采集show run,计算SHA256,存库并检测配置变化。"""
# 连接账号和密码直接填写在下面的连接参数中。

import hashlib       # 計算 SHA256
import re            # 正則表達式，從回顯中取出設定
import time          # time.sleep(5) 每輪間隔


from day04_01_multicmd import qytang_multicmd  # 复用第四天任务1的函数
from day05_01_router_model import RouterConfig, Session  # 复用任务1的表


def get_show_run(host, username, password):
    """获取配置并计算 hash"""
    # verbose=False → 不把 7000 多字的設定印在畫面上，只拿回傳值
    raw = qytang_multicmd(host, username, password,
                          ['terminal length 0', 'show running-config'],
                          verbose=False)
    # 正則：從「hostname 開頭的那一行」一直抓到「單獨一行的 end」
    #   ^ / $          → 搭配 MULTILINE，代表「每一行」的開頭 / 結尾
    #   .*?            → 搭配 DOTALL，. 也能比對換行；? 是非貪婪，抓到第一個 end 就停
    #   ( ... )        → 第 1 組，就是要保存的設定正文
    # 只取這一段 → 排除 "Building configuration..."、"Current configuration : N bytes"、
    #               提示符號等會變動的內容，HASH 才會穩定
    match = re.search(r'^(hostname[^\r\n]*\r?\n.*?^end)[ \t]*\r?$', raw,
                      flags=re.MULTILINE | re.DOTALL)
    if match is None:
        # 沒抓到完整設定（例如回顯被截斷）→ 停止這次備份，避免存進不完整的設定
        raise ValueError('没有收到从hostname到独立end行的完整配置,停止本次备份')
    # 待完成 2：
    #   match.group(0) → 整個比對結果（含括號外的空白、\r）
    #   match.group(1) → 第 1 組括號 → hostname ... end
    config = match.group(1)  # 待完成 2:从match中取出配置文本。
    # sha256 只吃 bytes → 字串先 .encode()；.hexdigest() → 轉成 64 個 16 進位字元
    config_hash = hashlib.sha256(config.encode()).hexdigest()  # 待完成 2：将配置文本转为字节后计算SHA256。
    return config, config_hash                 # 一次回傳兩個值（tuple）


def save_config(host, config, config_hash):
    """写入数据库（使用独立 session,避免事务残留）"""
    with Session() as session:
        # 待完成 3：左邊是資料表欄位名，右邊是這個函式收到的參數
        #   ORM 模型只接受「關鍵字參數」欄位名=值
        #   id、record_time 不用給 → 自動遞增 / 自動填當下時間
        record = RouterConfig(router_ip=host, router_config=config, config_hash=config_hash)  # 待完成 3：填入本次记录的数据。
        session.add(record)
        session.commit()                       # commit 才真正寫入


def get_latest_two_hashes(host):
    """查询最近两条记录"""
    with Session() as session:
        results = (session.query(RouterConfig)
                   # 待完成 4：只篩選這台設備
                   #   filter 寫法：類別.欄位 == 值（兩個等號）
                   #   filter_by 寫法：欄位=值（一個等號）
                   #   不篩選的話，多台設備時會拿 C8Kv1 跟 C8Kv2 的 HASH 比 → 誤報
                   .filter(RouterConfig.router_ip == host)  # 待完成 4：只筛选当前设备的记录。
                   .order_by(RouterConfig.id.desc())  # 最新的排第一
                   .limit(2)                          # 只取 2 筆：最新 + 上一筆
                   .all())                            # 執行查詢，回傳 list
        return results


if __name__ == '__main__':
    host     = '10.1.1.1'
    username = 'admin'
    password = 'Cisc0123'

    print(f"[*] 开始监控 {host} 的配置变化,每轮结束后等待 5 秒...\n")
    while True:                                          # 無限迴圈，Ctrl+C 停止
        config, config_hash = get_show_run(host, username, password)
        save_config(host, config, config_hash)           # 先存這一次
        records = get_latest_two_hashes(host)            # 再查最近兩筆（含剛存的）
        # records 是函式 return 回來的值；函式裡的 results 在這裡用不到（變數作用範圍）

        if len(records) < 2:
            # 資料庫裡只有 1 筆（第一次跑）→ 沒有東西可比，只印本次
            print(f"本次采集的HASH:{config_hash}")
        elif records[0].config_hash == records[1].config_hash:
            # 最新 == 上一筆 → 設定沒變
            print(f"本次采集的HASH:{config_hash}")  # 待完成 5：配置无变化,打印本次HASH。
        else:
            # 不同 → 告警；records[0] 是最新，records[1] 是上一筆
            print("==========配置发生变化==========")
            print(f"  THE MOST RECENT HASH  {records[0].config_hash}")  # 待完成 5：配置有变化，打印告警及前后两次HASH。
            print(f"  THE LAST HASH         {records[1].config_hash}")
        time.sleep(5)                                    # 每輪結束等 5 秒
