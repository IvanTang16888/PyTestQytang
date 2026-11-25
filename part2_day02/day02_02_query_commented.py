# ============================================================
# 第二部分 Day02 任務 2：從資料庫查回 BGP 規劃，印成報表
#
# 流程：
#   1. 查出所有 Router，依名稱排序（C8Kv1 → C8Kv2）
#   2. 每台印：標題、管理地址、本地 AS、Router ID
#   3. 再印 3 個表格：接口规划 / BGP邻居 / 宣告前缀
#   4. 全部透過 relationship 一層一層往下拿，不用自己寫 JOIN
# ============================================================

# 只需要 Router：其他表都從 router.xxx 點下去拿
# （注意 Cursor 會自動補 Neighbor 之類用不到的 import）
from bgp_models import session_factory , Router

Session = session_factory()

with Session() as session:
    # order_by(Router.name) = SQL 的 ORDER BY name；.all() 拿回 list
    routers = session.query(Router).order_by(Router.name).all()
    for router in routers:                                     # router = 這一圈的那台設備（小寫 = 一筆資料）
        print(f"{'='*20} {router.name} {'='*20}")              # '='*20 → 20 個等號
        print(f"管理地址: {router.host}")
        print(f"本地AS:   {router.bgp.local_as}")              # router.bgp → 這台的 BGP（1 份）
        print(f"Router ID: {router.bgp.router_id_value}")
        print()                                                # 空一行

        # ---- 表格 1：接口规划 ----
        print("接口规划")
        # 標題是固定文字 → {'Interface'} 要加引號；:<24 = 靠左、佔 24 格（不足補空格）
        # 最後一欄右邊沒東西要對齊 → 不設寬度
        print(f"{'Interface':<24}{'Address':<16}{'Mask':<16}{'Description'}")
        # sorted + key=lambda x: x.name → 依介面名稱排序（GigabitEthernet3 → Loopback100）
        for i in sorted(router.interfaces,key=lambda x: x.name):
            # 資料是變數 → {i.name} 不加引號
            print(f"{i.name:<24}{i.address:<16}{i.mask:<16}{i.description}")
        print()

        # ---- 表格 2：BGP邻居 ----
        print('BGP邻居')
        print(f"{'Peer IP':<16}{'Remote AS'}")
        # router.bgp.neighbors：router → 它的 bgp → bgp 底下的鄰居 list
        # （不能用大寫 Neighbor.xxx，那是整張表的欄位定義，不是這台的資料）
        for n in router.bgp.neighbors:
            print(f"{n.peer_ip:<16}{n.remote_as}")
        print()

        # ---- 表格 3：宣告前缀 ----
        print("宣告前缀")
        print(f"{'Prefix':<16}{'Mask'}")
        for p in router.bgp.networks:                          # 名稱要跟 bgp_models 的 networks 一模一樣（有 s）
            print(f"{p.prefix:<16}{p.mask}")
        print()                                                # 縮排 8 格：每台印完空一行，隔開下一台
