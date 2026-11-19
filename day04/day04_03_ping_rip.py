from day04_01_multicmd import qytang_multicmd
from day04_02_ping_check import ping_check
import getpass 

hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']
RIP_COMMANDS = [
    'configure terminal',
    'router rip',
    'version 2',
    'network 172.16.0.0',
    'end',
]

if __name__ == '__main__':
    
    pwd = getpass.getpass('SSH密码:')        # 只問一次密碼，3 台共用

    for ip in hosts:
        ok, rtt = ping_check(ip)
        if ok:
            print(f'[{ip}]' ' ping通，开始配置RIP')
            qytang_multicmd(ip,'admin',pwd,RIP_COMMANDS)
            print(f'[{ip}]' ' RIP命令执行完成')
        else:
            print(f'[{ip}]' ' ping不通，跳过SSH')