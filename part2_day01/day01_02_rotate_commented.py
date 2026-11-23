# ============================================================
# 第二部分 Day01 任務 2：產生模擬備份並清理過期檔案
#
# 流程：
#   1. 在腳本旁邊建立 backup/（已存在就報錯停止）
#   2. while True 每 3 秒：
#        建一個 backup_YYYY-MM-DD_HH-MM-SS.txt
#        → 刪掉「建立時間距現在超過 15 秒」的舊檔
#        → 印出保留列表
#   3. 按 Ctrl+C → 丟出 KeyboardInterrupt → 刪掉 backup/ 後結束
#
# 概念類似 ARP table 的 aging timer：超過時間的項目自動清掉
# ============================================================

from pathlib import Path   # 處理路徑、讀寫檔案
import shutil              # shutil.rmtree 刪除整個資料夾
import time,datetime       # time.sleep 控制間隔；datetime 處理時間（逗號一次借兩個）

backup_dir = Path(__file__).with_name('backup')   # 腳本同一層的 backup 資料夾

backup_dir.mkdir()          # 已存在 → FileExistsError，程式停止，不改原有內容

print('开始模拟备份; 按 Ctrl+C 停止并清理')

try:                        # try：平常要做的事
    while True:             # 條件永遠成立 → 一直重複，直到按 Ctrl+C
        # 取得現在時間；一定要加 () 才是「真的去看時鐘」
        now = datetime.datetime.now()
        # strftime：時間 → 文字，例如 backup_2026-11-23_23-16-29.txt
        #   %Y 年 %m 月 %d 日 %H 時 %M 分 %S 秒
        name = f"backup_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        (backup_dir / name).write_text('模拟备份内容\n')   # 模擬備份，內容隨意
        print(f'[+] 创建备份: {name}')                      # {name} 要放在引號裡面
        # 逐一檢查 backup/ 裡的每個檔案
        for file in sorted(backup_dir.iterdir()):
            # strptime：文字 → 時間（strftime 的反向）
            #   file.stem = 檔名去掉 .txt → backup_2026-11-23_23-16-14
            file_time = datetime.datetime.strptime(file.stem, 'backup_%Y-%m-%d_%H-%M-%S')
            # now - file_time = 這個檔案「多久以前」建立的
            # timedelta(seconds=15) = 「15 秒」這段時間長度
            if now - file_time > datetime.timedelta(seconds=15):
                file.unlink()                                  # 刪除這一個檔案（像 rm 檔案）
                print(f'[-] 删除过期备份: {file.name}')
        # 縮排 8 格、跟 for 對齊 → 所有檔案都檢查完才印一次
        # 列表推導式：把剩下的檔案只取檔名，收集成清單
        keep = [f.name for f in sorted(backup_dir.iterdir())]
        # ', '.join(清單)：用「逗號 + 空格」把檔名串成一行
        print('保留列表: ' + ', '.join(keep))
        time.sleep(3)       # 永遠放在迴圈最後：這一圈做完才休息 3 秒

except KeyboardInterrupt:   # 按 Ctrl+C 時 Python 丟出 KeyboardInterrupt，在這裡接住

    print('收到 Ctrl+C')
    shutil.rmtree(backup_dir)      # 刪除整個 backup/
    print('backup/ 目录已清理')
