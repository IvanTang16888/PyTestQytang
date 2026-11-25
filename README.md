# PyTestQytang — AIOps Vibe Coding 2026 作業

網路工程師的 Python / AIOps 課程練習，依上課天數分資料夾。

| 資料夾 | 主題 |
|---|---|
| [day01/](day01/) | Python 基礎：字串、列表、字典、格式化輸出 |
| [day02/](day02/) | 正則表達式解析網路設備輸出 |
| [day03/](day03/) | SQLAlchemy ORM：設備 Inventory 系統 |
| [day04/](day04/) | Paramiko 多命令、ping 檢查、自動設定 RIP |
| [day05/](day05/) | ORM 設定備份表、show run HASH 變化偵測 |
| [part2_day01/](part2_day01/) | 第二部分 Day01：批量檢查 shutdown、模擬備份輪替（pathlib、datetime、shutil） |
| [part2_day02/](part2_day02/) | 第二部分 Day02：BGP 規劃資料入庫與查詢（PostgreSQL 容器、SQLAlchemy 5 表關聯） |

## 環境

- Python 3.13（虛擬環境）
- 套件清單：[requirements.txt](requirements.txt)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
