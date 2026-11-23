from pathlib import Path
import shutil
import time,datetime

backup_dir = Path(__file__).with_name('backup')

backup_dir.mkdir()

print('开始模拟备份; 按 Ctrl+C 停止并清理')

try:
    while True:
        now = datetime.datetime.now()
        name = f"backup_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        (backup_dir / name).write_text('模拟备份内容\n')
        print(f'[+] 创建备份: {name}')
        for file in sorted(backup_dir.iterdir()):
            file_time = datetime.datetime.strptime(file.stem, 'backup_%Y-%m-%d_%H-%M-%S')
            if now - file_time > datetime.timedelta(seconds=15):
                file.unlink()
                print(f'[-] 删除过期备份: {file.name}')
        keep = [f.name for f in sorted(backup_dir.iterdir())]
        print('保留列表: ' + ', '.join(keep))
        time.sleep(3)

except KeyboardInterrupt:

    print('收到 Ctrl+C')
    shutil.rmtree(backup_dir)
    print('backup/ 目录已清理')















