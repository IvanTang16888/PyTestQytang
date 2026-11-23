# 第二部分 Day 01 — 批量檢查 shutdown、模擬備份輪替

> 第二部分「運維數據與設備配置」的第一天作業。作業檔名重新從 `day01_` 編號，所以放在 `part2_day01/`，跟第一部分的 `day01/` 分開。

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day01_01_audit.py](day01_01_audit.py) | 把 4 份模擬設定寫成檔案，找出含有單獨 `shutdown` 的檔名，最後清理目錄 | `Path(__file__).with_name()`、`mkdir()`、`dict.items()`、`write_text` / `read_text`、`splitlines()`、`strip()`、`break`、`shutil.rmtree` |
| [day01_02_rotate.py](day01_02_rotate.py) | 每 3 秒產生一份備份，刪除超過 15 秒的舊檔，Ctrl+C 後清理目錄 | `while True`、`time.sleep`、`datetime.now()`、`strftime` / `strptime`、`timedelta`、`unlink()`、列表推導式、`', '.join()`、`try / except KeyboardInterrupt` |

> 每題有兩個版本：`xxx.py` 是交作業用的原始程式碼（無註解），`xxx_commented.py` 是加上中文註解的學習版，兩者執行結果相同。只用 Python 標準函式庫。

## 執行方式

```bash
source .venv/bin/activate
cd part2_day01
python day01_01_audit.py     # 跑完自動刪除 backup/
python day01_02_rotate.py    # 跑 20 秒以上才會看到刪除紀錄，按 Ctrl+C 停止
```

## 執行結果

```
$ python day01_01_audit.py
发现包含 shutdown 接口的设备配置文件:
R1_config.txt
SW1_config.txt
backup/ 目录已清理

$ python day01_02_rotate.py
开始模拟备份; 按 Ctrl+C 停止并清理
[+] 创建备份: backup_2026-11-23_23-19-00.txt
保留列表: backup_2026-11-23_23-19-00.txt
……
[+] 创建备份: backup_2026-11-23_23-19-15.txt
[-] 删除过期备份: backup_2026-11-23_23-19-00.txt
保留列表: backup_2026-11-23_23-19-03.txt, backup_2026-11-23_23-19-06.txt, backup_2026-11-23_23-19-09.txt, backup_2026-11-23_23-19-12.txt, backup_2026-11-23_23-19-15.txt
^C收到 Ctrl+C
backup/ 目录已清理
```

## 筆記

- `mkdir()` 不加 `exist_ok=True`：目錄已存在就丟出 `FileExistsError` 並停止，原有內容不會被改，一行就做到「已存在就報錯」的要求。
- `for name, content in files.items()`：`name` 接 key（檔名），`content` 接 value（內容）。
- `line.strip() == 'shutdown'`：用「完全等於」比對，`no shutdown` 才不會被誤判。
- `break` 只跳出最近的那一層迴圈（`for line`），然後繼續檢查下一個檔案。
- `strftime` 把時間變文字（f = format），`strptime` 把文字變回時間（p = parse），兩邊的格式字串要一致。
- `datetime.datetime.now()` 要加括號才會取得現在時間；day05 ORM 的 `default=datetime.datetime.now` 不加括號，是把函式交給資料庫，寫入時才呼叫。
- `time.sleep(3)` 放在迴圈最後一行：這一圈做完才休息。
- 縮排：每往內一層多 4 格；在 Cursor 用 `Tab` / `Shift+Tab` 調整整行，`Alt+↑` / `Alt+↓` 上下移動整行。
- f-string 的 `{變數}` 一定要放在引號裡面。
- 注意 Cursor 自動補全偷加的 import（這次是 `from pickle import APPEND`）。
