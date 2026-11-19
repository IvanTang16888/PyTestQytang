# Day 04 — Paramiko 多命令、ping 檢查、自動設定 RIP

| 檔案 | 任務 | 練習重點 |
|---|---|---|
| [day04_01_multicmd.py](day04_01_multicmd.py) | 同一個 SSH 互動終端依序執行多條命令 | `invoke_shell()`、`sendall()` / `recv()`、`str.encode()` / `bytes.decode()`、`getpass` |
| [day04_02_ping_check.py](day04_02_ping_check.py) | ping 檢查主機是否可達，回傳 `(True, RTT)` / `(False, None)` | `pythonping`、`.success()`、`.rtt_avg_ms`、多值回傳與拆包、`f'{rtt:.2f}'` |
| [day04_03_ping_rip.py](day04_03_ping_rip.py) | 先 ping，通了才 SSH 設定 RIP，不通就跳過 | `import` 重複使用函式、`if __name__ == '__main__'`、變數作用範圍 |

> 每題有兩個版本：`xxx.py` 是交作業用的原始程式碼（無註解），`xxx_commented.py` 是加上中文註解的學習版，兩者執行結果相同。

## 執行方式

```bash
source .venv/bin/activate      # 先啟動虛擬環境（需要 paramiko、pythonping）
cd day04
python day04_01_multicmd.py    # 輸入 SSH 密碼
python day04_02_ping_check.py  # 需要 raw socket 權限，見下方說明
python day04_03_ping_rip.py    # 會實際修改 C8Kv1 / C8Kv2 的設定
```

**pythonping 權限：**一般帳號會出現 `PermissionError: [Errno 1] Operation not permitted`，二選一：

```bash
sudo .venv/bin/python day04/day04_02_ping_check.py                  # 每次用 sudo
sudo setcap cap_net_raw+ep "$(readlink -f .venv/bin/python)"        # 只給 Python 發 ICMP 的權限，設一次即可
```

## 執行結果

```
$ python day04_02_ping_check.py
10.1.1.1   可达   RTT: 3.04 ms
10.1.1.2   可达   RTT: 13.91 ms
10.1.1.3   不可达

$ python day04_03_ping_rip.py
SSH密码:
[10.1.1.1] ping通，开始配置RIP
...
C8Kv1#
[10.1.1.1] RIP命令执行完成
[10.1.1.2] ping通，开始配置RIP
...
C8Kv2#
[10.1.1.2] RIP命令执行完成
[10.1.1.3] ping不通，跳过SSH
```

驗證：`show running-config | section router rip` → 兩台都出現 `router rip / version 2 / network 172.16.0.0`。

## 筆記

- `exec_command()` 每條命令各開一個通道，狀態不延續；`invoke_shell()` 是互動式終端，`configure terminal` → `router rip` 這種有前後關係的命令要用它。
- `ssh.connect()` 的第 2 個位置參數是 `port`，所以帳密要用關鍵字參數 `username=` / `password=`。
- `sendall()` 只收 bytes → `(cmd + '\n').encode()`；`recv()` 收回來也是 bytes → `.decode()`。
- `rs.success` 是函式本身，放在 `if` 裡永遠為 True；要寫 `rs.success()` 才是真正的結果。
- ping 不通時 `rtt_avg_ms` 是 timeout 值（2000），不是真的 RTT，所以要回傳 `None`。
- 函式回傳原始資料（數字），要印的時候再格式化；轉成字串後 `{rtt:.2f}` 會報錯。
- 函式裡的變數（例如 `rs`）在函式外面用不到，外面只拿得到 `return` 的值。
- 注意 Cursor 自動補全偷加的 import（例如 `from base64 import encode`、`from sqlite3 import paramstyle`）。
