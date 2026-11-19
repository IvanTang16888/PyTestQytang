from pythonping import ping

def ping_check(host, count=1, timeout=2):
    """ping通返回(True, 平均延迟毫秒)，不通返回(False, None)。"""
   
    rs = ping(host,count=count,timeout=timeout,verbose=False)
    
    if rs.success():
        return(rs.success(),rs.rtt_avg_ms)
    else:
        return False,None

if __name__ == '__main__':
    hosts = ['10.1.1.1', '10.1.1.2', '10.1.1.3']
    for host in hosts:
        ok, rtt = ping_check(host)
        if ok:
            print(f'{host}   可达   RTT: {rtt:.2f} ms')
        else:
            print(f'{host}   不可达')

