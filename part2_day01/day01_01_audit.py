from pathlib import Path
import shutil

files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}

backup_dir = Path(__file__).with_name('backup')

backup_dir.mkdir()

for name,content in files.items():
    backup_dir_name = backup_dir / name
    backup_dir_name.write_text(content)


print('发现包含 shutdown 接口的设备配置文件:')


for file in sorted(backup_dir.iterdir()):
    for line in file.read_text().splitlines():    
        if line.strip() == 'shutdown':
            print(file.name)
            break
shutil.rmtree(backup_dir)

print('backup/ 目录已清理')




