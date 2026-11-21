# Day 05 — ORM 設定備份表、show run HASH 變化偵測

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day05_01_router_model.py](day05_01_router_model.py) | 用 ORM 建立 `router_config` 設定備份表 | `Column(型別, 約束)`、`primary_key` / `autoincrement`、`nullable=False`、`index=True`、`default=datetime.datetime.now`、`inspect`、`flush` / `rollback` |
| [day05_02_config_monitor.py](day05_02_config_monitor.py) | 每 5 秒採集 show run、算 SHA256、存庫，設定變化時告警 | `match.group(1)`、`hashlib.sha256(str.encode()).hexdigest()`、`filter(類別.欄位 == 值)`、`order_by(id.desc()).limit(2)` |
| [day04_01_multicmd.py](day04_01_multicmd.py) | 第四天任務 1 的互動式 SSH 函式（複製一份，供任務 2 import） | — |

> 每題有兩個版本：`xxx.py` 是交作業用的原始程式碼（無註解），`xxx_commented.py` 是加上中文註解的學習版，兩者執行結果相同。

## 執行方式

```bash
source .venv/bin/activate          # 先啟動虛擬環境（需要 SQLAlchemy、paramiko）
cd day05
python day05_01_router_model.py    # 建表並驗證表結構；router_config.db 建在目前目錄
python day05_02_config_monitor.py  # 持續監控 10.1.1.1，Ctrl+C 停止
```

**任務 2 實驗步驟**（另開視窗登入 C8Kv1）：

```
configure terminal
ip host d5-test 192.0.2.1          ← 第 1 次告警
end
configure terminal
no ip host d5-test 192.0.2.1       ← 第 2 次告警，HASH 回到最初的值
end
```

## 執行結果

```
[*] 开始监控 10.1.1.1 的配置变化,每轮结束后等待 5 秒...

本次采集的HASH:e3efcfb694a641e54e54d9443ff139315a48b6c254c5f6a1ad0f15556927be7e
本次采集的HASH:e3efcfb694a641e54e54d9443ff139315a48b6c254c5f6a1ad0f15556927be7e
==========配置发生变化==========
  THE MOST RECENT HASH  7dc6fb4f848430d1ae1a5d8812f14fb08a63b89035474cdd59fc8178dfa94d30
  THE LAST HASH         e3efcfb694a641e54e54d9443ff139315a48b6c254c5f6a1ad0f15556927be7e
本次采集的HASH:7dc6fb4f848430d1ae1a5d8812f14fb08a63b89035474cdd59fc8178dfa94d30
==========配置发生变化==========
  THE MOST RECENT HASH  e3efcfb694a641e54e54d9443ff139315a48b6c254c5f6a1ad0f15556927be7e
  THE LAST HASH         7dc6fb4f848430d1ae1a5d8812f14fb08a63b89035474cdd59fc8178dfa94d30
本次采集的HASH:e3efcfb694a641e54e54d9443ff139315a48b6c254c5f6a1ad0f15556927be7e
```

## 筆記

- 舊寫法的型別要放在 `Column( )` 小括號的第一個：`Column(String(64), ...)`；不要跟新寫法 `Mapped[str]` 混用，少了型別會報 `NullType` 錯誤。
- `String` 要大寫；Python 區分大小寫，錯誤訊息的 `Did you mean` 通常就是答案。
- `default=datetime.datetime.now` 不加括號。`sqlalchemy` 的 `now` 是資料庫端的函式，SQLite 沒有。
- `create_all` 只建立不存在的表，不會修改已存在的表；改欄位後要把舊的 `.db` 改名備份再重建。
- `flush()` 先送出 INSERT（拿得到 id），`rollback()` 再撤銷 → 測試資料不會留下來。
- 正則只取 `hostname ... end` 這一段，排除會變動的 `Current configuration : N bytes`，HASH 才會穩定。
- `sha256()` 只吃 bytes → `str.encode()`。
- 主程式裡要用 `records`（函式回傳值），不是函式內部的 `results`。
- lab 每天重新部署，C8Kv 的 host key 會變；在 Linux 上 `ssh` 出現 `REMOTE HOST IDENTIFICATION HAS CHANGED` 時，用 `ssh-keygen -R 10.1.1.1` 清除舊紀錄。Paramiko 的 `AutoAddPolicy()` 則不受影響。
- 注意 Cursor 自動補全偷加的 import（這次是 `from curses import raw`、`from typing import Self`、`from sqlalchemy.sql.functions import now`）。
