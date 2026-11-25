from bgp_models import session_factory , Router

Session = session_factory()

with Session() as session:
    routers = session.query(Router).order_by(Router.name).all()
    for router in routers:
        print(f"{'='*20} {router.name} {'='*20}")
        print(f"管理地址: {router.host}")
        print(f"本地AS:   {router.bgp.local_as}")
        print(f"Router ID: {router.bgp.router_id_value}")
        print()
        print("接口规划")
        print(f"{'Interface':<24}{'Address':<16}{'Mask':<16}{'Description'}")
        for i in sorted(router.interfaces,key=lambda x: x.name):
            print(f"{i.name:<24}{i.address:<16}{i.mask:<16}{i.description}")
        print()
        print('BGP邻居')
        print(f"{'Peer IP':<16}{'Remote AS'}")
        for n in router.bgp.neighbors:
            print(f"{n.peer_ip:<16}{n.remote_as}")
        print()
        print("宣告前缀")
        print(f"{'Prefix':<16}{'Mask'}")
        for p in router.bgp.networks:
            print(f"{p.prefix:<16}{p.mask}")
        print()
           
