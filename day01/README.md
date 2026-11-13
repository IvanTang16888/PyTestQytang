# Day 01 — Python 基礎：字串、列表、字典、格式化輸出

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day01_02_slice.py](day01_02_slice.py) | 拆出介面類型與編號 | 字串切片 `[0:15]`、`[-5:]` |
| [day01_03_string_methods.py](day01_03_string_methods.py) | 清理版本字串 | `strip()`、`upper()`、`replace()` |
| [day01_04_device_card.py](day01_04_device_card.py) | 印出設備資訊卡 | 變數、字串串接、對齊 |
| [day01_05_random_ipv4.py](day01_05_random_ipv4.py) | 產生隨機 IPv4 位址 | `random.randint()`、`str()` 型別轉換 |
| [day01_06_ip_plan.py](day01_06_ip_plan.py) | IP 規劃表 | 字典列表、`for` 迴圈、f-string 對齊 `{:<18}` |
| [day01_07_interfaces.py](day01_07_interfaces.py) | 介面狀態表 | `str.format()` 對齊、`"-" * 20` |
| [day01_08_syslog.py](day01_08_syslog.py) | 解析 Syslog 介面狀態 | `re.search()`、捕獲組 `group(1)` / `group(2)` |

## 執行方式

```bash
source .venv/bin/activate      # 先啟動虛擬環境
python day01/day01_06_ip_plan.py
```

## 筆記

- 中文字在終端機佔 2 格寬，用 `:<N` 對齊時含中文的欄位會歪掉。
- `re.match()` 只從字串開頭比對；`re.search()` 會在整個字串裡找。
