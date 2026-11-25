# ============================================================
# 第二部分 Day02 任務 1：把 bgp_plan.json 寫進 PostgreSQL
#
# 流程：
#   1. 讀 bgp_plan.json → plan（list，每個元素是一台設備的 dict）
#   2. 每台先查資料庫：name 已存在就跳過（可重複執行，不會重複寫入）
#   3. 用 relationship 把 Router → Interface / BGP → Neighbor / Network 串起來
#   4. session.add(router) 一次加入，commit 時外鍵會自動填好
#   5. 印出 5 張表的筆數
# ============================================================

import json
# 從自己寫的 bgp_models.py 拿 session 工廠和 5 個類別
from bgp_models import session_factory, Router, Interface, BGP, Neighbor, Network

# encoding='utf-8'：檔案裡有中文時才不會亂碼；with 結束自動關檔
with open('bgp_plan.json',encoding='utf-8') as f:
    plan = json.load(f)          # JSON 文字 → Python list / dict

Session = session_factory()      # 建表（若不存在）+ 拿到 Session 工廠

with Session() as session:       # 開一個連線，with 結束自動關閉
    for device in plan:          # device = 一台設備的 dict
        # filter_by(name=...) = SQL 的 WHERE name = ...；.first() 取第一筆，沒有就是 None
        exist = session.query(Router).filter_by(name=device['name']).first()
        if exist:                # 有找到 → 已經寫過
            print(f"{device['name']} 已存在，跳过")
            continue             # 跳過這台，直接下一圈（不是 break）

        # 建 Router 物件（還沒進資料庫，id 也還沒有）
        router = Router(name=device['name'], host=device['host'])

        # 介面：append 到 router.interfaces → commit 時自動填 router_id
        for i in device['interfaces']:
            router.interfaces.append(Interface(name=i['name'], address=i['address'], mask=i['mask'], description=i['description']))

        # BGP 只有 1 份（uselist=False）→ 用 = 指定，不是 append
        # JSON 的 router_id 放進 router_id_value 欄位
        router.bgp = BGP(local_as=device['local_as'], router_id_value=device['router_id'])

        # 鄰居、宣告前綴掛在 router.bgp 底下 → commit 時自動填 bgp_id
        for n in device['neighbors']:
            router.bgp.neighbors.append(Neighbor(peer_ip=n['peer_ip'], remote_as=n['remote_as']))
        for p in device['networks']:
            router.bgp.networks.append(Network(prefix=p['prefix'], mask=p['mask']))

        # 只 add 最上層的 router，掛在它底下的物件會一起被加入
        session.add(router)
        print(f"{device['name']} 已录入")

    session.commit()             # 迴圈全部跑完才一次寫進資料庫

    # .count() 要加括號才會真的去數
    print(f"Router={session.query(Router).count()}")
    print(f"Interface={session.query(Interface).count()}")
    print(f"BGP={session.query(BGP).count()}")
    print(f"Neighbor={session.query(Neighbor).count()}")
    print(f"Network={session.query(Network).count()}")
