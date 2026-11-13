# Day 02 — 正則表達式解析網路設備輸出

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day02_01_mac_table.py](day02_01_mac_table.py) | 解析交換機 MAC 表 | `re.match()`、`\d{1,4}`、`[0-9a-fA-F]{4}`、`\s+` |
| [day02_02_asa_conn.py](day02_02_asa_conn.py) | 解析 ASA 連線資訊 | 多個捕獲組、IP:Port 拆分 |
| [day02_03_route_gateway.py](day02_03_route_gateway.py) | 從 `route -n` 找預設閘道 | `re.search()` 在多行文字裡搜尋、跳脫 `\.` |
| [day02_04_asa_dict.py](day02_04_asa_dict.py) | ASA 連線表轉成字典 | `split("\n")` 逐行處理、元組當字典 key、`.items()` |
| [day02_05_port_sort.py](day02_05_port_sort.py) | 介面名稱依數字排序 | `sorted(key=lambda ...)`、`int()` 轉換、元組比較 |

> 每題有兩個版本：`xxx.py` 是交作業用的原始程式碼（無註解），`xxx_commented.py` 是加上中文註解的學習版，兩者執行結果相同。

## 執行方式

```bash
source .venv/bin/activate      # 先啟動虛擬環境
python day02/day02_05_port_sort.py
```

## 筆記

- 正則沒比對到時會回傳 `None`，接著呼叫 `.group()` 就會出現
  `'NoneType' object has no attribute 'group'`。先檢查空格和 `\s+`。
- 字串排序是逐字元比較（`'13' < '7'`），要轉成 `int` 才會依數字大小排。
- 長正則可以用括號包起來、拆成多行，Python 會自動把相鄰的字串接起來。
