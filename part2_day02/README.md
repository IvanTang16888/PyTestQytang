# 第二部分 Day 02 — BGP 規劃資料入庫與查詢（PostgreSQL + SQLAlchemy）

> 把 2 台 C8Kv 的 eBGP 規劃（`bgp_plan.json`）寫進 PostgreSQL 的 5 張關聯表，再透過 relationship 一層一層查回來，印成報表。

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [compose.yml](compose.yml) | 起一個 PostgreSQL 16 容器，只開 `127.0.0.1:15435` | `image`、`ports`、`environment`、具名 volume |
| [bgp_plan.json](bgp_plan.json) | 題目給的輸入資料（C8Kv1 AS65001 ↔ C8Kv2 AS65002） | — |
| [bgp_models.py](bgp_models.py) | 5 張表的 ORM 模型 + `session_factory()` | `declarative_base`、`ForeignKey`、`relationship`、`uselist=False`、`unique=True` |
| [day02_01_seed.py](day02_01_seed.py) | 任務 1：讀 JSON 寫入資料庫，已存在就跳過，印出各表筆數 | `json.load`、`filter_by().first()`、`continue`、`append` 子物件、`session.add` / `commit`、`count()` |
| [day02_02_query.py](day02_02_query.py) | 任務 2：查回每台的管理地址、AS、Router ID，以及介面 / 鄰居 / 前綴三個表格 | `order_by`、`router.bgp.neighbors` 串接、`sorted(key=lambda)`、f-string `:<16` 對齊 |

> 每支 `.py` 都有 `_commented.py` 學習版（加中文註解），執行結果相同。

## 表結構

```
aiops_router ─┬─< aiops_interface      (router_id → aiops_router.id)
              └── aiops_bgp            (router_id → aiops_router.id, unique，一對一)
                   ├─< aiops_neighbor  (bgp_id → aiops_bgp.id)
                   └─< aiops_network   (bgp_id → aiops_bgp.id)
```

## 執行方式

```bash
cd part2_day02
docker compose up -d                 # 起資料庫（容器 part2_day02-postgres-1，資料存在 volume bgp-data）
source ../.venv/bin/activate         # 需要 sqlalchemy、psycopg2-binary
python day02_01_seed.py              # 第一次：已录入；再跑一次：已存在，跳过
python day02_02_query.py
```

> 不要用 `docker compose down -v`，`-v` 會連 volume 一起刪掉，資料就沒了。

## 執行結果

```
$ python day02_01_seed.py
C8Kv1 已录入
C8Kv2 已录入
Router=2
Interface=4
BGP=2
Neighbor=2
Network=2

$ python day02_01_seed.py
C8Kv1 已存在，跳过
C8Kv2 已存在，跳过
Router=2
Interface=4
BGP=2
Neighbor=2
Network=2

$ python day02_02_query.py
==================== C8Kv1 ====================
管理地址: 10.1.1.1
本地AS:   65001
Router ID: 10.101.1.1

接口规划
Interface               Address         Mask            Description
GigabitEthernet3        172.16.2.1      255.255.255.0   EBGP-TO-C8Kv2
Loopback100             10.101.1.1      255.255.255.255 BGP-PREFIX

BGP邻居
Peer IP         Remote AS
172.16.2.2      65002

宣告前缀
Prefix          Mask
10.101.1.1      255.255.255.255

==================== C8Kv2 ====================
管理地址: 10.1.1.2
本地AS:   65002
Router ID: 10.102.2.2

接口规划
Interface               Address         Mask            Description
GigabitEthernet3        172.16.2.2      255.255.255.0   EBGP-TO-C8Kv1
Loopback100             10.102.2.2      255.255.255.255 BGP-PREFIX

BGP邻居
Peer IP         Remote AS
172.16.2.1      65001

宣告前缀
Prefix          Mask
10.102.2.2      255.255.255.255
```

## 筆記

- `relationship` 不是資料庫欄位，是 Python 端的捷徑：`router.bgp.neighbors` = 這台 → 它的 BGP → BGP 底下的鄰居。真正存關聯的是 `ForeignKey` 欄位。
- `uselist=False`：一對一，`router.bgp` 回傳單一物件，所以 seed 用 `router.bgp = BGP(...)`，不是 `append`。
- 大寫 `Neighbor` 是類別（整張表的設計圖），小寫 `n` 是迴圈拿到的一筆資料；要印資料就用 `n.peer_ip`。
- `for` 後面的名字自己取，同一個名字在不同迴圈重用不會衝突（後面的會蓋掉前面的），但用 `i` / `n` / `p` 比較好讀。
- f-string 裡：固定文字要加引號 `{'Mask'}`；變數不加 `{p.mask}`。`(Mask)` 會照字面印出，`{Mask}` 會報 `NameError`。
- `:<16` 只管印出來佔幾格，讓下一欄對齊；最後一欄右邊沒東西，不用設。
- 題目的中文是簡體（`邻居`、`前缀`），打成繁體就對不上。
- relationship 的名稱要一模一樣：`networks` 少一個 s 就會報錯。
- `create_all()` 只建不存在的表，不會刪資料；改了欄位不會自動更新已存在的表。
- 又一次 Cursor 自動補 import（這次是 `Neighbor`），寫完記得看最上面。
