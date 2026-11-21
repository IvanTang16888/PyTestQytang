import time, paramiko,getpass

cmd_list = [
    'terminal length 0',
    'show version | include Software,',
    'show running-config | include hostname',
]

def qytang_multicmd(ip,username,password,cmd_list, wait_time=2 , verbose=True):
    """在同一个SSH交互终端依次执行cmd_list,返回全部回显文本。"""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,username=username,password=password,look_for_keys=False, allow_agent=False)

    chan = ssh.invoke_shell()
    time.sleep(1); welcome = chan.recv(65535)

    output = ''
    for cmd in cmd_list:
        chan.sendall((cmd +'\n').encode())
        time.sleep(wait_time)
        result = chan.recv(65535).decode()
        output += result
        if verbose:
            print(result)
    ssh.close()
    return output


if __name__ == '__main__':
    pwd = getpass.getpass('SSH密码:')
    qytang_multicmd('10.1.1.1', 'admin', pwd, cmd_list)

