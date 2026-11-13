# Day 03 — SQLAlchemy ORM：設備 Inventory 系統

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day03_01_inventory.py](day03_01_inventory.py) | 設備資產清單存進 SQLite，選單查詢 | `declarative_base()`、`Column`、`session.add/commit`、`filter_by()` 精確查詢、`like("%關鍵字%")` 模糊查詢、`__repr__` |

> 每題有兩個版本：`xxx.py` 是交作業用的原始程式碼（無註解），`xxx_commented.py` 是加上中文註解的學習版，兩者執行結果相同。

## 執行方式

```bash
source .venv/bin/activate      # 先啟動虛擬環境（需要 SQLAlchemy 2.0.44）
cd day03
python day03_01_inventory.py   # 資料庫 device_inventory.db 會建在目前目錄
realpath -e device_inventory.db
```

## 筆記

- ORM：一個類別 = 一張表，一個物件 = 一筆資料，不用自己寫 SQL。
- `default=datetime.now`（不加括號）→ 寫入時才取時間；加了括號會變成程式啟動時的固定時間。
- 只在 `count() == 0` 時寫入初始資料 → 重複執行不會重複新增，入庫時間也不會變。
- 精確查詢用 `filter_by(欄位=值)`；模糊查詢用 `filter(類別.欄位.like(...))`。
- `.db` 檔已加入 `.gitignore`，不會被上傳。
