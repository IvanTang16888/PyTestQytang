# ============================================================
# 第二部分 Day01 任務 1：批量檢查設定中的 shutdown
#
# 流程：
#   1. 在腳本旁邊建立 backup/（已存在就報錯停止，不動原有內容）
#   2. 把 files 字典的 4 份模擬設定寫成 4 個 .txt
#   3. 依檔名排序，一行一行檢查，找出「單獨的 shutdown」（no shutdown 不算）
#   4. 刪除整個 backup/
# ============================================================

from pathlib import Path   # 從 pathlib 工具箱只拿出 Path（處理路徑、讀寫檔案）
import shutil              # 整個 shutil 工具箱（用 shutil.rmtree 刪除整個資料夾）

# 題目給的輸入：key = 檔名，value = 檔案內容（\n 是換行）
files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}

# __file__ = 這支程式自己的路徑；.with_name('backup') = 換成旁邊的 backup 資料夾
# （跟 netmiko_show_client.py 的 Path(__file__).with_name('work') 同一招）
backup_dir = Path(__file__).with_name('backup')

# 不加 exist_ok=True → backup/ 已存在時會丟出 FileExistsError，程式停止，
# 後面的寫檔都不會執行 → 原有內容保持不變（題目要求）
backup_dir.mkdir()

# .items() 每一圈交出一組 key : value → name 接 key（檔名），content 接 value（內容）
for name,content in files.items():
    backup_dir_name = backup_dir / name        # 用 / 組路徑 → backup/R1_config.txt
    backup_dir_name.write_text(content)        # 把文字內容寫進這個檔案


print('发现包含 shutdown 接口的设备配置文件:')


# iterdir() 列出 backup/ 裡所有檔案（像 ls）；sorted() 依檔名排序 → R1, R2, R3, SW1
for file in sorted(backup_dir.iterdir()):
    # read_text() 讀出整份內容；splitlines() 依換行切成一行一行
    for line in file.read_text().splitlines():
        # strip() 去掉前後空白：' shutdown' → 'shutdown' ✅；' no shutdown' → 'no shutdown' ❌
        if line.strip() == 'shutdown':
            print(file.name)                   # file 是完整路徑，.name 只取檔名
            break                              # 找到一次就夠了，跳出 for line，換下一個檔案
# 靠最左邊 → 全部檢查完才執行一次：刪除整個資料夾（像 rm -r backup）
shutil.rmtree(backup_dir)

print('backup/ 目录已清理')
