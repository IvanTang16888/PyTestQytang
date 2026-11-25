import json
from bgp_models import session_factory, Router, Interface, BGP, Neighbor, Network

with open('bgp_plan.json',encoding='utf-8') as f:
    plan = json.load(f)

Session = session_factory()

with Session() as session:
    for device in plan:
        exist = session.query(Router).filter_by(name=device['name']).first()
        if exist:
            print(f"{device['name']} 已存在，跳过")
            continue
        router = Router(name=device['name'], host=device['host'])
        for i in device['interfaces']:
            router.interfaces.append(Interface(name=i['name'], address=i['address'], mask=i['mask'], description=i['description']))
        router.bgp = BGP(local_as=device['local_as'], router_id_value=device['router_id'])
        for n in device['neighbors']:
            router.bgp.neighbors.append(Neighbor(peer_ip=n['peer_ip'], remote_as=n['remote_as']))
        for p in device['networks']:
            router.bgp.networks.append(Network(prefix=p['prefix'], mask=p['mask']))
        session.add(router)
        print(f"{device['name']} 已录入")
    session.commit()
    print(f"Router={session.query(Router).count()}")
    print(f"Interface={session.query(Interface).count()}")
    print(f"BGP={session.query(BGP).count()}")
    print(f"Neighbor={session.query(Neighbor).count()}")
    print(f"Network={session.query(Network).count()}")
